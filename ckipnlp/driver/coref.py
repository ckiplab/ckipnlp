#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides built-in coreference resolution driver.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

import numpy as _np

from treelib import (
    Tree as _Tree,
)

from ckipnlp.container import (
    TextParagraph as _TextParagraph,
    SegParagraph as _SegParagraph,
    ParseParagraph as _ParseParagraph,
    NerParagraph as _NerParagraph,
    CorefToken as _CorefToken,
    CorefSentence as _CorefSentence,
    CorefParagraph as _CorefParagraph,
)

from ckipnlp.data.conparse import (
    APPOSITION_ROLES as _APPOSITION_ROLES,
)

from ckipnlp.data.coref import (
    HUMAN_WORDS as _HUMAN_WORDS,
    PRONOUN_3RD_WORDS as _PRONOUN_3RD_WORDS,
    SELF_WORDS as _SELF_WORDS,
)

from .base import (
    BaseDriver as _BaseDriver,
)

################################################################################################################################

class CkipCorefChunker(_BaseDriver):  # pylint: disable=too-few-public-methods
    """The CKIP coreference resolution driver.

    Arguments
    ---------
        lazy : bool
            Lazy initialize the driver.

    .. method:: __call__(*, conparse)

        Apply coreference delectation.

        Parameters
            **conparse** (:class:`~ckipnlp.container.parse.ParseParagraph`) — The constituency-parsing sentences.

        Returns
            **coref** (:class:`~ckipnlp.container.coref.CorefParagraph`) — The coreference results.
    """

    driver_type = 'coref_chunker'
    driver_family = 'default'
    driver_inputs = None

    def _init(self):
        pass

    def _call(self, *, conparse):
        assert isinstance(conparse, _ParseParagraph)

        # Convert to tree structure
        tree_list = [
            [
                (clause.to_tree(), clause.delim,)
                for clause in sent
            ] for sent in conparse
        ]

        # Find coreference
        coref_tree = self._get_coref(tree_list)

        # # Get results
        coref = self._get_result(tree_list, coref_tree=coref_tree)

        return coref

    ########################################################################################################################

    @classmethod
    def _get_coref(cls, tree_list):

        coref_tree = _Tree()
        coref_tree.create_node(identifier=0)
        dummy_id = (-1, -1, -1)
        coref_tree.create_node(identifier=dummy_id, parent=0, data=True)

        name2node = {}  # name => ((sent_id, clause_id,), (node_id, is_prepend))

        curr_source = None    # the current coref source
        last_source = None    # the last coref source
        last_subject = None   # the last coref subject

        last_sent_pos = None  # the POS-tag of last sentence

        # Find coref
        for sent_id, clause_list in enumerate(tree_list):
            for clause_id, (tree, _) in enumerate(clause_list):
                tree_key = (sent_id, clause_id,)

                if tree is None:
                    continue
                curr_sent_pos = tree[tree.root].data.pos

                # Get relations
                appositions = []
                for rel in tree.get_relations():
                    if rel.relation.data.role in _APPOSITION_ROLES:
                        appositions.append(((rel.head.identifier, False), (rel.tail.identifier, False),))

                # Get sources/targets
                node_keys = {}
                for node_key in cls._get_sources(tree): # Source
                    node_keys[node_key] = True
                for node_key in cls._get_targets(tree): # Target
                    node_keys[node_key] = False
                subject_keys = set(cls._get_subjects(tree)) # Subject

                for node_key, ntype in sorted(node_keys.items()):
                    if ntype: # Assign ref_id to sources
                        source = tree[node_key[0]]
                        curr_source = (tree_key, node_key,)

                        parent_id = name2node.get(source.data.word, None)
                        if parent_id:
                            coref_tree.create_node(identifier=(tree_key, node_key,), parent=parent_id, data=True)
                        else:
                            name2node[source.data.word] = (tree_key, node_key,)
                            coref_tree.create_node(identifier=(tree_key, node_key,), parent=0, data=True)

                    else: # Link targets to previous sources
                        if node_key[1] and last_subject:
                            coref_tree.create_node(identifier=(tree_key, node_key,), parent=last_subject, data=False)
                        if not node_key[1]:
                            if curr_source and tree[node_key[0]].data.word in _SELF_WORDS:
                                coref_tree.create_node(identifier=(tree_key, node_key,), parent=curr_source, data=False)
                            elif last_source:
                                coref_tree.create_node(identifier=(tree_key, node_key,), parent=last_source, data=False)
                            else:
                                coref_tree.create_node(identifier=(tree_key, node_key,), parent=dummy_id, data=False)

                # Merge apposition (apposition role)
                for head_key, tail_key in appositions:
                    head_key = (tree_key, head_key,)
                    tail_key = (tree_key, tail_key,)

                    if coref_tree.contains(head_key) and coref_tree.contains(tail_key):
                        if coref_tree.is_ancestor(head_key, tail_key) or \
                           coref_tree.is_ancestor(tail_key, head_key):
                            continue

                        if coref_tree[head_key].data:  # Head is a source
                            coref_tree.move_node(tail_key, head_key)
                        elif coref_tree[tail_key].data:  # Tail is a source
                            coref_tree.move_node(head_key, tail_key)
                        else:
                            coref_tree.move_node(tail_key, head_key)

                # Merge apposition (NP sentences)
                if curr_sent_pos == 'NP' and last_sent_pos == 'NP' and last_subject:
                    for node_key, ntype in node_keys.items():
                        if ntype: # Merge sources only
                            source_id = (tree_key, node_key,)
                            if coref_tree.contains(source_id):
                                coref_tree.move_node(source_id, last_subject)

                # Update subject
                if curr_sent_pos in ('NP', 'S'):
                    last_subject = None
                    for node_key, ntype in sorted(node_keys.items(), key=lambda x: x[::-1]):
                        if node_key in subject_keys:
                            last_subject = (tree_key, node_key,)
                            break

                # Update last
                last_source = curr_source
                last_sent_pos = curr_sent_pos

        # Remove dummy node
        coref_tree.remove_node(dummy_id)

        return coref_tree


    @classmethod
    def _get_result(cls, tree_list, *, coref_tree):

        # Assign coref ID
        node2coref = {}  # ((sent_id, clause_id,), (node_id, is_prepend)) => ref_id
        sources = set()  # ((sent_id, clause_id,), (node_id, is_prepend))

        for ref_id, coref_source in enumerate(coref_tree.children(coref_tree.root)):
            tree_key, node_key = coref_source.identifier
            sources.add((tree_key, node_key,))
            for tree_key, node_key in coref_tree.expand_tree(coref_source.identifier):
                node2coref[tree_key, node_key] = ref_id

        # Generate result
        tokens_list = _CorefParagraph()
        for sent_id, clause_list in enumerate(tree_list):
            tokens = _CorefSentence()
            tokens_list.append(tokens)

            for clause_id, (tree, delim,) in enumerate(clause_list):
                tree_key = (sent_id, clause_id,)

                if tree is not None:
                    nodes = tree.leaves()

                    for node in nodes:
                        key = (tree_key, (node.identifier, True),)
                        ref_id = node2coref.get(key, -1)
                        if ref_id >= 0:
                            tokens.append(_CorefToken(  # pylint: disable=no-value-for-parameter
                                word=None,
                                idx=(clause_id, None,),
                                coref=(ref_id, 'zero'),
                            ))

                        key = (tree_key, (node.identifier, False),)
                        ref_id = node2coref.get(key, -1)
                        if ref_id >= 0:
                            tokens.append(_CorefToken(  # pylint: disable=no-value-for-parameter
                                word=node.data.word,
                                idx=(clause_id, node.identifier,),
                                coref=(ref_id, 'source' if key in sources else 'target',),
                            ))
                        else:
                            tokens.append(_CorefToken(  # pylint: disable=no-value-for-parameter
                                word=node.data.word,
                                idx=(clause_id, node.identifier,),
                                coref=None,
                            ))
                if delim:
                    tokens.append(_CorefToken(  # pylint: disable=no-value-for-parameter
                        word=delim,
                        idx=(clause_id, None,),
                        coref=None,
                    ))

        return tokens_list

    ########################################################################################################################

    @staticmethod
    def transform_ws(*, text, ws, ner):
        """Transform word-segmented sentence lists (create a new instance)."""
        assert isinstance(text, _TextParagraph)
        assert isinstance(ws, _SegParagraph)
        assert isinstance(ner, _NerParagraph)

        ws_new = []
        for line, line_ws, line_ner in zip(text, ws, ner):
            line_bi = _np.zeros(len(line)+1, dtype=_np.bool)
            line_bi[0] = True
            line_bi[_np.cumsum(list(map(len, line_ws)))] = True
            for _, _, (idx0, idx1,) in line_ner:
                line_bi[[idx0, idx1]] = True
                line_bi[idx0+1:idx1] = False
            idxs = _np.where(line_bi)[0]
            ws_new.append([line[idx0:idx1] for idx0, idx1 in zip(idxs[:-1], idxs[1:])])
        return _SegParagraph.from_list(ws_new)

    @staticmethod
    def transform_pos(*, ws, pos, ner):
        """Transform pos-tag sentence lists (modify in-place)."""
        assert isinstance(ws, _SegParagraph)
        assert isinstance(pos, _SegParagraph)
        assert isinstance(ner, _NerParagraph)

        for line_ws, line_pos, line_ner in zip(ws, pos, ner):
            idxmap = {idx: i for i, idx in enumerate(_np.cumsum(list(map(len, line_ws))))}
            for token in line_ner:
                if token.ner == 'PERSON':
                    line_pos[idxmap[token.idx[1]]] = 'Nb'

    ########################################################################################################################

    @classmethod
    def _get_sources(cls, tree):
        """Get sources of a tree

        Parameters
        ----------
            tree : :class:`~ckipnlp.container.util.parse_tree.ParseTree`
                the constituency parsing tree.

        Yields
        ------
            int
                the identifier of source nodes.
            bool
                prepend this node or not.

        Notes
        -----
            A node can be a coreference source if either:

            1. POS-tag is `Nb`
            2. is one of the human words from E-HowNet

        """
        for node in tree.leaves():
            if cls._is_human_word(node):
                yield node.identifier, False

    @classmethod
    def _get_targets(cls, tree):
        """Get targets of a tree

        Parameters
        ----------
            tree : :class:`~ckipnlp.container.util.parse_tree.ParseTree`
                the constituency parsing tree.

        Yields
        ------
            int
                the identifier of source nodes.
            bool
                prepend this node or not.

        Notes
        -----
            A node can be a coreference target if either:

            1. POS-tag is `Nh`
            2. is one of the pronoun words from E-HowNet

        """
        root = tree[tree.root]
        leaves = tree.leaves()

        if root.data.pos == 'VP':
            if leaves[0].data.pos.startswith('Cb'): # coref will be inserted after this Cb node
                yield leaves[1].identifier, True
            else: # coref will be inserted in front of the whole sentence
                yield leaves[0].identifier, True

        for node in leaves:
            if cls._is_pronoun_word(node):
                yield node.identifier, False

    ########################################################################################################################

    @classmethod
    def _get_subjects(cls, tree):
        """Get subjects of a tree

        Parameters
        ----------
            tree : :class:`~ckipnlp.container.util.parse_tree.ParseTree`
                the constituency parsing tree.

        Yields
        ------
            int
                the identifier of subject node.
            bool
                prepend this node or not.
        """
        for node in tree.get_subjects():
            yield node.identifier, False

    ########################################################################################################################

    @staticmethod
    def _is_human_word(node):
        return node.data.pos.startswith('Nb') or node.data.pos.startswith('N') and node.data.word in _HUMAN_WORDS

    @staticmethod
    def _is_pronoun_word(node):
        return node.data.pos.startswith('Nh') or node.data.pos.startswith('N') and node.data.word in _PRONOUN_3RD_WORDS
