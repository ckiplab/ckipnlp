#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides built-in coreference resolution driver.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import numpy as _np

from treelib import (
    Tree as _Tree,
)

from ckipnlp.container import (
    TextParagraph as _TextParagraph,
    SegParagraph as _SegParagraph,
    ParsedParagraph as _ParsedParagraph,
    ParsedTree as _ParsedTree,
    NerParagraph as _NerParagraph,
    CorefToken as _CorefToken,
    CorefSentence as _CorefSentence,
    CorefParagraph as _CorefParagraph,
)

from ckipnlp.data.parsed import (
    APPOSITION_ROLES as _APPOSITION_ROLES,
)

from ckipnlp.data.coref import (
    HUMAN_WORDS as _HUMAN_WORDS,
    PRONOUN_3RD_WORDS as _PRONOUN_3RD_WORDS,
    SELF_WORDS as _SELF_WORDS,
)

from .base import (
    BaseDriver as _BaseDriver,
    DriverType as _DriverType,
    DriverFamily as _DriverFamily,
)

################################################################################################################################

class CkipCorefChunker(_BaseDriver):  # pylint: disable=too-few-public-methods
    """The CKIP coreference resolution driver.

    Arguments
    ---------
        lazy : bool
            Lazy initialize underlay object.

    .. py:method:: __call__(*, parsed)

        Apply coreference delectation.

        Parameters
            **parsed** (:class:`ParsedParagraph <ckipnlp.container.parsed.ParsedParagraph>`) — The parsed-sentences.

        Returns
            **coref** (:class:`CorefParagraph <ckipnlp.container.coref.CorefParagraph>`) — The coreference results.
    """

    driver_type = _DriverType.COREF_CHUNKER
    driver_family = _DriverFamily.BUILTIN

    def _call(self, *, parsed):
        assert isinstance(parsed, _ParsedParagraph)

        # Convert to tree structure
        tree_list = list(map(_ParsedTree.from_text, parsed))

        # Find coreference
        coref_tree = self._get_coref(tree_list)

        # Get results
        coref = self._get_result(tree_list, coref_tree=coref_tree)

        return coref

    def _init(self):
        pass

    @classmethod
    def _get_coref(cls, tree_list):

        coref_tree = _Tree()
        coref_tree.create_node(identifier=0)
        dummy_id = (-1, -1)
        coref_tree.create_node(identifier=dummy_id, parent=0, data=True)

        name2node = {}  # name => (tree_id, node_id)

        curr_source = None    # the current coref source
        last_source = None    # the last coref source
        last_subject = None   # the last coref subject

        last_sent_pos = None  # the POS-tag of last sentence

        # Find coref
        for tree_id, tree in enumerate(tree_list):

            curr_sent_pos = tree[tree.root].data.pos

            # Get relations
            appositions = []
            for rel in tree.get_relations():
                if rel.relation.data.role in _APPOSITION_ROLES:
                    appositions.append((rel.head.identifier, rel.tail.identifier,))

            # Get sources/targets
            node_ids = {}
            for nid in cls._get_sources(tree): # Source
                node_ids[nid] = True
            for nid in cls._get_targets(tree): # Target
                node_ids[nid] = False
            subject_ids = set(cls._get_subjects(tree)) # Subject

            for nid, ntype in sorted(node_ids.items()):
                if ntype: # Assign ref_id to sources
                    source = tree[nid]
                    curr_source = (tree_id, nid,)

                    parent_id = name2node.get(source.data.word, None)
                    if parent_id:
                        coref_tree.create_node(identifier=(tree_id, nid,), parent=parent_id, data=True)
                    else:
                        name2node[source.data.word] = (tree_id, nid,)
                        coref_tree.create_node(identifier=(tree_id, nid,), parent=0, data=True)

                else: # Link targets to previous sources
                    if nid < 0 and last_subject:
                        coref_tree.create_node(identifier=(tree_id, nid,), parent=last_subject, data=False)
                    if nid >= 0:
                        if curr_source and tree[nid].data.word in _SELF_WORDS:
                            coref_tree.create_node(identifier=(tree_id, nid,), parent=curr_source, data=False)
                        elif last_source:
                            coref_tree.create_node(identifier=(tree_id, nid,), parent=last_source, data=False)
                        else:
                            coref_tree.create_node(identifier=(tree_id, nid,), parent=dummy_id, data=False)

            # Merge apposition (apposition role)
            for head_id, tail_id in appositions:
                head_id = (tree_id, head_id,)
                tail_id = (tree_id, tail_id,)

                if coref_tree.contains(head_id) and coref_tree.contains(tail_id):
                    if coref_tree.is_ancestor(head_id, tail_id) or \
                       coref_tree.is_ancestor(tail_id, head_id):
                        continue

                    if coref_tree[head_id].data:  # Head is a source
                        coref_tree.move_node(tail_id, head_id)
                    elif coref_tree[tail_id].data:  # Tail is a source
                        coref_tree.move_node(head_id, tail_id)
                    else:
                        coref_tree.move_node(tail_id, head_id)

            # Merge apposition (NP sentences)
            if curr_sent_pos == 'NP' and last_sent_pos == 'NP' and last_subject:
                for nid, ntype in node_ids.items():
                    if ntype: # Merge sources only
                        source_id = (tree_id, nid,)
                        if coref_tree.contains(source_id):
                            coref_tree.move_node(source_id, last_subject)

            # Update subject
            if curr_sent_pos in ('NP', 'S'):
                last_subject = None
                for nid, ntype in sorted(node_ids.items(), key=lambda x: x[::-1]):
                    if nid in subject_ids:
                        last_subject = (tree_id, nid,)
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
        node2coref = {}  # (tree_id, node_id) => ref_id
        sources = set()  # (tree_id, node_id)

        for ref_id, coref_source in enumerate(coref_tree.children(coref_tree.root)):
            tree_id, node_id = coref_source.identifier
            sources.add((tree_id, node_id,))
            for tree_id, node_id in coref_tree.expand_tree(coref_source.identifier):
                node2coref[tree_id, node_id] = ref_id

        # Generate result
        tokens_list = _CorefParagraph()
        for tree_id, tree in enumerate(tree_list):
            tokens = _CorefSentence()
            tokens_list.append(tokens)

            nodes = tree.leaves()

            if (tree_id, -1) in node2coref:
                ref_id = node2coref[tree_id, -1]
                tokens.append(_CorefToken(  # pylint: disable=no-value-for-parameter
                    word=None,
                    idx=None,
                    coref=(ref_id, 'zero'),
                ))

            elif (tree_id, -2) in node2coref:
                # The pos of the first leaf node starts with 'Cb'. e.g. 而且、但是、然而
                node = nodes.pop(0)
                tokens.append(_CorefToken(  # pylint: disable=no-value-for-parameter
                    word=node.data.word,
                    idx=node.identifier,
                    coref=None,
                ))

                ref_id = node2coref[tree_id, -2]
                tokens.append(_CorefToken(  # pylint: disable=no-value-for-parameter
                    word=None,
                    idx=None,
                    coref=(ref_id, 'zero'),
                ))

            for node in nodes:
                ref_id = node2coref.get((tree_id, node.identifier,), -1)
                if ref_id >= 0:
                    tokens.append(_CorefToken(  # pylint: disable=no-value-for-parameter
                        word=node.data.word,
                        idx=node.identifier,
                        coref=(ref_id, 'source' if (tree_id, node.identifier,) in sources else 'target',),
                    ))
                else:
                    tokens.append(_CorefToken(  # pylint: disable=no-value-for-parameter
                        word=node.data.word,
                        idx=node.identifier,
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
            tree : :class:`ParsedTree <ckipnlp.container.util.parsed_tree.ParsedTree>`
                the parser tree.

        Yields
        ------
            int
                the identifier of source nodes.

        Notes
        -----
            A node can be a coreference source if either:

            1. POS-tag is `Nb`
            2. is one of the human words from E-HowNet

        """
        for node in tree.leaves():
            if cls._is_human_word(node):
                yield node.identifier

    @classmethod
    def _get_targets(cls, tree):
        """Get targets of a tree

        Parameters
        ----------
            tree : :class:`ParsedTree <ckipnlp.container.util.parsed_tree.ParsedTree>`
                the parser tree.

        Yields
        ------
            int
                the identifier of target nodes.
            -2
                if the tree is not VP and pos of the first leaf node starts with 'Cb'
            -1
                if the tree is not VP

        Notes
        -----
            A node can be a coreference target if either:

            1. POS-tag is `Nh`
            2. is one of the pronoun words from E-HowNet

        """
        root = tree[tree.root]
        leaves = tree.leaves()

        if root.data.pos == 'VP':
            if leaves[0].data.pos.startswith('Cb'):
                yield -2 # coref will be inserted after this Cb node
            else:
                yield -1 # coref will be inserted in front of the whole sentence

        for node in leaves:
            if cls._is_pronoun_word(node):
                yield node.identifier

    ########################################################################################################################

    @classmethod
    def _get_subjects(cls, tree):
        """Get subjects of a tree

        Parameters
        ----------
            tree : :class:`ParsedTree <ckipnlp.container.util.parsed_tree.ParsedTree>`
                the parser tree.

        Yields
        ------
            int
                the identifier of subject node.
        """
        for node in tree.get_subjects():
            yield node.identifier

    ########################################################################################################################

    @staticmethod
    def _is_human_word(node):
        return node.data.pos.startswith('Nb') or node.data.pos.startswith('N') and node.data.word in _HUMAN_WORDS

    @staticmethod
    def _is_pronoun_word(node):
        return node.data.pos.startswith('Nh') or node.data.pos.startswith('N') and node.data.word in _PRONOUN_3RD_WORDS

    @staticmethod
    def _getitem_deep(obj, idx0, idx1):
        return obj[idx0][idx1]

    @staticmethod
    def _setitem_deep(obj, idx0, idx1, value):
        obj[idx0][idx1] = value

    ########################################################################################################################
