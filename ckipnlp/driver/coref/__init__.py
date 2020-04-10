#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import numpy as _np

from ckipnlp.container import (
    SegParagraph as _SegParagraph,
    ParsedParagraph as _ParsedParagraph,
    ParsedTree as _ParsedTree,
)

from ..base import (
    BaseDriver as _BaseDriver,
    DriverType as _DriverType,
    DriverKind as _DriverKind,
)

from .data import *

from colored import *

def print_spam(*args, **kwargs):
    print(stylize(*args, fg('magenta') + attr('dim')), **kwargs)

def print_debug(*args, **kwargs):
    print(stylize(*args, fg('blue')), **kwargs)

def print_verbose(*args, **kwargs):
    print(stylize(*args, fg('magenta')), **kwargs)

def print_info(*args, **kwargs):
    print(stylize(*args, fg('cyan')), **kwargs)

def print_notice(*args, **kwargs):
    print(stylize(*args, fg('cyan') + attr('bold')), **kwargs)

def print_warning(*args, **kwargs):
    print(stylize(*args, fg('yellow') + attr('bold')), **kwargs)

def print_success(*args, **kwargs):
    print(stylize(*args, fg('green') + attr('bold')), **kwargs)

def print_error(*args, **kwargs):
    print(stylize(*args, fg('red') + attr('bold')), **kwargs)

def print_fatal(*args, **kwargs):
    print(stylize(*args, bg('red') + attr('bold')), **kwargs)

################################################################################################################################

class CkipCorefChunker(_BaseDriver,  # pylint: disable=too-few-public-methods
    driver_type=_DriverType.COREF_CHUNKER,
    driver_kind=_DriverKind.BUILTIN,
):
    """The CKIP co-reference driver."""

    def _call(self, *, parsed):
        assert isinstance(parsed, _ParsedParagraph)

        trees = list(map(_ParsedTree.from_text, parsed))

        # Find subject
        for tree in trees:
            tree.show()
            for sub in self.get_subject(tree):
                print_verbose(sub)

        return None

    def _init(self):
        pass

    def transform_ws(self, text, ws, ner):
        """Transform word-segmented sentence lists (create a new instance)."""
        ws_new = []
        for line, line_ws, line_ner in zip(text, ws, ner):
            line_bi = _np.zeros(len(line)+1, dtype=_np.bool)
            line_bi[0] = True
            line_bi[_np.cumsum(list(map(len, line_ws)))] = True
            for _, _, (i0, i1,) in line_ner:
                line_bi[[i0, i1]] = True
                line_bi[i0+1:i1] = False
            idxs = _np.where(line_bi)[0]
            ws_new.append([line[i0:i1] for i0, i1 in zip(idxs[:-1], idxs[1:])])
        return _SegParagraph.from_list(ws_new)

    def transform_pos(self, ws, pos, ner):
        """Transform pos-tag sentence lists (modify in-place)."""
        for line_ws, line_pos, line_ner in zip(ws, pos, ner):
            idxmap = {idx: i for i, idx in enumerate(_np.cumsum(list(map(len, line_ws))))}
            for netype, _, (_, i1,) in line_ner:
                if netype == 'PERSON':
                    line_pos[idxmap[i1]] = 'Nb'

    def get_subject(self, tree):
        """Get subjects of a tree

        Parameters
        ----------
        tree : :class:`ckipnlp.util.parser.ParserTree`
            the parser tree.

        Yields
        ------
        :class:`ckipnlp.util.parser.ParserNode`
            the subject nodes.

        Notes
        -----
            A node can be a Coreference source if one of the following is true:
                1. `pos` starts with `Nb'
                2. `word` is one of the `human_words` from E-HowNet
        """

        for root in tree.children(0):
            for head in tree.get_heads(root.identifier):
                print_spam(head)
                if root.data.pos == 'NP' and (head.data.word in HUMAN_WORDS or head.data.pos.startswith('Nb')):
                    yield head
                elif root.data.pos != 'VP':
                    for subroot in tree.children(root.identifier):
                        print_debug(subroot)
                        for subhead in tree.get_heads(subroot.identifier):
                            print_spam(subhead)
                            foundSub = subroot.data.role in SUBJECT_ROLES or \
                                      (subhead.identifier < head.identifier and subroot.data.role in NEUTRAL_ROLES)
                            if foundSub and (subhead.data.word in HUMAN_WORDS or subhead.data.pos.startswith('Nb')):
                                yield subhead
