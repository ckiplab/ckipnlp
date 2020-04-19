#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import numpy as _np

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

from ..base import (
    BaseDriver as _BaseDriver,
    DriverType as _DriverType,
    DriverKind as _DriverKind,
)

from ._data import *

################################################################################################################################

from colored import *  # pylint: disable=wrong-import-order

def print_spam(*args, **kwargs):
    print(stylize(' '.join(map(str, args)), fg('magenta') + attr('dim')))  # pylint: disable=no-value-for-parameter

def print_debug(*args):
    print(stylize(' '.join(map(str, args)), fg('blue')))  # pylint: disable=no-value-for-parameter

def print_verbose(*args):
    print(stylize(' '.join(map(str, args)), fg('magenta')))  # pylint: disable=no-value-for-parameter

def print_info(*args):
    print(stylize(' '.join(map(str, args)), fg('cyan')))  # pylint: disable=no-value-for-parameter

def print_notice(*args):
    print(stylize(' '.join(map(str, args)), fg('cyan') + attr('bold')))  # pylint: disable=no-value-for-parameter

def print_warning(*args):
    print(stylize(' '.join(map(str, args)), fg('yellow') + attr('bold')))  # pylint: disable=no-value-for-parameter

def print_success(*args):
    print(stylize(' '.join(map(str, args)), fg('green') + attr('bold')))  # pylint: disable=no-value-for-parameter

def print_error(*args):
    print(stylize(' '.join(map(str, args)), fg('red') + attr('bold')))  # pylint: disable=no-value-for-parameter

def print_fatal(*args):
    print(stylize(' '.join(map(str, args)), bg('red') + attr('bold')))  # pylint: disable=no-value-for-parameter

################################################################################################################################

class CkipCorefChunker(_BaseDriver):  # pylint: disable=too-few-public-methods
    """The CKIP co-reference driver."""

    driver_type = _DriverType.COREF_CHUNKER
    driver_kind = _DriverKind.BUILTIN

    def _call(self, *, parsed):
        assert isinstance(parsed, _ParsedParagraph)

        # Convert to tree structure
        tree_list = list(map(_ParsedTree.from_text, parsed))

        # Find co-reference
        nid2coref_list, coref2term = self._get_coref(tree_list)

        print(nid2coref_list)
        print(coref2term)
        print()

        for k1, nid2coref in enumerate(nid2coref_list):
            for k2, v in nid2coref.items():
                if k2 >= 0:
                    print(tree_list[k1][k2], v)
                else:
                    print(k1, k2, v)
        print()

        for v in coref2term.values():
            if v:
                k1, k2, n = v
                print(nid2coref_list[k1][k2], n)
        print()

        # Form results
        result = self._get_result(tree_list, nid2coref_list=nid2coref_list, coref2term=coref2term)

        for s in result:
            # print(s)
            ss = []
            for w in s:
                if not w.coref:
                    ss.append(w.word)
                else:
                    ss.append(f'{w.word}_{w.coref[0]}')
            print_success(*ss)

    def _init(self):
        pass

    @classmethod
    def _get_coref(cls, tree_list):

        nid2coref_list = [{} for _ in tree_list]  # tree_id => {tree_id => ref_id}
        coref2term = {-1: None}  # ref_id => (tree_id, node_id)

        # Reset flags
        last_subject_rid = -1  # coref id of the last coref source
        last_person_rid = -1   # coref id of the last coref source whose pos starts with 'Nb'
        last_pronoun_rid = -1  # coref id of the last coref source who is a pronoun words

        coref_flag = False    # True if a subject is found, False if an S is found but no subject is detected
        pronoun_flag = False  # True when VP can coref to last_pronoun_rid

        # Find coref
        for i, (tree, nid2coref) in enumerate(zip(tree_list, nid2coref_list)):
            print_error()
            print_error('='*8, i, '='*8)

            tree.show()
            root = tree[tree.root]

            # Get subjects/pronouns/targets
            subjects = tuple(cls.get_subject(tree))
            pronouns = tuple(cls.get_pronoun(tree))
            target_ids = tuple(cls.get_target(tree))
            subjects = tuple(sub for sub in subjects if sub not in pronouns)
            print_success('subject', subjects)
            print_success('pronoun', pronouns)
            print_success('target', target_ids)

            # Update flags
            if subjects:
                coref_flag = True
                pronoun_flag = False
            elif root.data.pos != 'VP' and not target_ids:
                coref_flag = False
                pronoun_flag = False
            elif not coref_flag and pronouns:
                # VP can coref to last_pronoun_rid
                pronoun_flag = True

            print_notice('F:coref', coref_flag)
            print_notice('F:pronoun', pronoun_flag)

            # VP can coref to previous pronoun
            if pronoun_flag and pronouns:
                for pronoun in pronouns:
                    last_subject_rid += 1
                    last_pronoun_rid = last_subject_rid
                    coref2term[last_pronoun_rid] = (i, pronoun.identifier, pronoun,)
            elif pronoun_flag:
                for target_id in target_ids:
                    if target_id < 0:  # if target is a VP
                        # find the closest coref source
                        if last_pronoun_rid >= 0:
                            nid2coref[tid] = last_pronoun_rid

            if not coref_flag:
                # set to empty so that there won't be coref in this tree
                target_ids = []

             # subject found
            if subjects:
                for subject in subjects:
                    last_subject_rid += 1

                    if subject.data.pos.startswith('Nb'):
                        last_person_rid = last_subject_rid

                    coref2term[last_subject_rid] = (i, subject.identifier, subject,)

                    # map the coref source to itself
                    nid2coref[subject.identifier] = last_subject_rid

                    if target_ids:
                        for target_id in target_ids:
                            if target_id > subject.identifier: # coref to the same tree
                                if last_person_rid >= 0:
                                    nid2coref[target_id] = last_person_rid
                            elif target_id > -1: # coref to previous source
                                if last_subject_rid == last_person_rid:
                                    if last_subject_rid > 0:
                                        nid2coref[target_id] = last_subject_rid - 1
                                elif last_person_rid >= 0:
                                    nid2coref[target_id] = last_person_rid
                            else: # target_id == -1 or -2 is a VP, coref to any kind of subject
                                nid2coref[target_id] = last_subject_rid

             # no subject found
            else:
                for target_id in target_ids:
                    if target_id <= -1: # if target is a VP
                        # find the closest coref source
                        if last_subject_rid >= 0:
                            nid2coref[target_id] = last_subject_rid
                    else: # if it's an Nhaa or human
                        # find the closest Nba coref source
                        if last_person_rid >= 0:
                            nid2coref[target_id] = last_person_rid

            print()

        return nid2coref_list, coref2term

    @classmethod
    def _get_result(cls, tree_list, *, nid2coref_list, coref2term):
        tokens_list = _CorefParagraph()

        for i, (tree, nid2coref) in enumerate(zip(tree_list, nid2coref_list)):
            tokens = _CorefSentence()
            tokens_list.append(tokens)

            nodes = tree.leaves()

            print_error()
            print_error('='*8, i, '='*8)
            print_notice(nid2coref)
            print_verbose(nodes)

            if -1 in nid2coref:
                ref_id = nid2coref[-1]
                _, _, ref_node = coref2term[ref_id]
                tokens.append(_CorefToken(
                    word=None,
                    idx=None,
                    coref=ref_id,
                    role='zero',
                ))

            elif -2 in nid2coref:
                # The pos of the first leaf node starts with 'Cb'. e.g. 而且、但是、然而
                node = nodes.pop(0)
                tokens.append(_CorefToken(
                    word=node.data.word,
                    idx=node.identifier,
                    coref=None,
                ))

                ref_id = nid2coref[-2]
                _, _, ref_node = coref2term[ref_id]
                tokens.append(_CorefToken(
                    word=None,
                    idx=None,
                    coref=(ref_id, 'zero'),
                ))

            for node in nodes:
                if node.identifier in nid2coref:

                    ref_id = nid2coref[node.identifier]
                    _, _, ref_node = coref2term[ref_id]
                    tokens.append(_CorefToken(
                        word=node.data.word,
                        idx=node.identifier,
                        coref=(ref_id, 'source' if node.identifier == ref_node.identifier else 'target',),
                    ))
                else:
                    tokens.append(_CorefToken(
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
            for ner in line_ner:
                if ner.ner == 'PERSON':
                    line_pos[idxmap[ner.idx[1]]] = 'Nb'

    ########################################################################################################################

    @classmethod
    def get_subject(cls, tree, *, root_id=None):
        """Get subjects of a tree

        Parameters
        ----------
            tree : :class:`ParsedTree <ckipnlp.container.tree.parsed.ParsedTree>`
                the parser tree.

        Yields
        ------
            :class:`ParsedTree <ckipnlp.container.tree.parsed.ParsedNode>`
                the subject nodes.

        Notes
        -----
            A node can be a co-reference source if either:

            1. POS-tag is `Nb'
            2. is one of the human words from E-HowNet

            A node can be a co-reference source if either:

            1. is a head of `NP`
            2. is a head of a subnode of root with subject role
            3. is a head of a subnode of root with neutral role and precede the head of root

        """
        if root_id is None:
            root_id = tree.root
        root = tree[root_id]

        if root.data.pos == 'NP':
            for head in tree.get_heads(root.identifier):
                if cls._is_human_word(head):
                    yield head

        elif root.data.pos != 'VP':
            for head in tree.get_heads(root.identifier):
                for subroot in tree.children(root.identifier):
                    for subhead in tree.get_heads(subroot.identifier):
                        found_sub = subroot.data.role in _SUBJECT_ROLES or \
                                   (subroot.data.role in _NEUTRAL_ROLES and subhead.identifier < head.identifier)
                        if found_sub and cls._is_human_word(subhead):
                            yield subhead

        for subroot in tree.children(root.identifier):
            if subroot.data.pos == 'S':
                yield from cls.get_subject(tree, root_id=subroot.identifier)

    @classmethod
    def get_pronoun(cls, tree, *, root_id=None):
        """Get pronouns of a tree

        Parameters
        ----------
            tree : :class:`ParsedTree <ckipnlp.container.tree.parsed.ParsedTree>`
                the parser tree.

        Yields
        ------
            :class:`ParsedTree <ckipnlp.container.tree.parsed.ParsedNode>`
                the pronoun nodes.

        Notes
        -----
            A node can be a co-reference source if either:

            1. POS-tag is `Nh'
            2. is one of the pronoun words from E-HowNet

            A node can be a co-reference source if either:

            1. is a head of `NP`
            2. is a head of a subnode of root with subject role
            3. is a head of a subnode of root with neutral role and precede the head of root

        """
        if root_id is None:
            root_id = tree.root
        root = tree[root_id]

        if root.data.pos == 'NP':
            for head in tree.get_heads(root.identifier):
                if cls._is_pronoun_word(head):
                    yield head

        elif root.data.pos != 'VP':
            for head in tree.get_heads(root.identifier):
                for subroot in tree.children(root.identifier):
                    for subhead in tree.get_heads(subroot.identifier):
                        found_sub = subroot.data.role in _SUBJECT_ROLES or \
                                   (subroot.data.role in _NEUTRAL_ROLES and subhead.identifier < head.identifier)
                        if found_sub and cls._is_pronoun_word(subhead):
                            yield subhead

        for subroot in tree.children(root.identifier):
            if subroot.data.pos == 'S':
                yield from cls.get_pronoun(tree, root_id=subroot.identifier)

    @classmethod
    def get_target(cls, tree, *, root_id=None):
        """Get target_ids of a tree

        Parameters
        ----------
            tree : :class:`ParsedTree <ckipnlp.container.tree.parsed.ParsedTree>`
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
            A node can be a co-reference target if either:

            1. is one of the pronoun words from E-HowNet

        """
        if root_id is None:
            root_id = tree.root
        root = tree[root_id]
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

    @staticmethod
    def _is_human_word(node):
        return node.data.word in _HUMAN_WORDS or node.data.pos.startswith('Nb')

    @staticmethod
    def _is_pronoun_word(node):
        return node.data.word in _PRONOUN_WORDS or node.data.pos.startswith('Nh')

    ########################################################################################################################
