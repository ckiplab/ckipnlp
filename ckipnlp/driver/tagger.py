#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from ckipnlp.container import (
    TextSentenceList as _TextSentenceList,
    SegSentenceList as _SegSentenceList,
    WsSentenceList as _WsSentenceList,
    NerSentenceList as _NerSentenceList,
)

from ckipnlp.util.data import (
    get_tagger_data as _get_tagger_data,
)

from .base import (
    BaseDriver as _BaseDriver
)

################################################################################################################################

class CkipTaggerSeg(_BaseDriver):  # pylint: disable=too-few-public-methods
    """The CKIP word segmentation driver with CkipTagger backend."""

    def __init__(self):
        super().__init__()

        import ckiptagger
        self._core = ckiptagger.WS(_get_tagger_data())

    def __call__(self, *, text):
        assert isinstance(text, _TextSentenceList)

        seg_list = self._core(text)
        seg = _SegSentenceList.from_list(seg_list)

        return seg

class CkipTaggerPos(_BaseDriver):  # pylint: disable=too-few-public-methods
    """The CKIP part-of-speech tagging driver with CkipTagger backend."""

    def __init__(self):
        super().__init__()

        import ckiptagger
        self._core = ckiptagger.POS(_get_tagger_data())

    def __call__(self, *, seg):
        assert isinstance(seg, _SegSentenceList)

        pos_list = self._core(seg)
        ws = _WsSentenceList.from_word_pos(seg, pos_list)

        return ws

class CkipTaggerNer(_BaseDriver):  # pylint: disable=too-few-public-methods
    """The CKIP named entity recognition driver with CkipTagger backend."""

    def __init__(self):
        super().__init__()

        import ckiptagger
        self._core = ckiptagger.NER(_get_tagger_data())

    def __call__(self, *, ws):
        assert isinstance(ws, _WsSentenceList)

        seg = ws.to_word()
        pos = ws.to_pos()
        ner_list = self._core(seg, pos)

        ner = _NerSentenceList.from_tagger(ner_list)

        return ner
