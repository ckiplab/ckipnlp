#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from ckipnlp.container import (
    TextParagraph as _TextParagraph,
    SegParagraph as _SegParagraph,
    NerParagraph as _NerParagraph,
)

from ckipnlp.util.data import (
    get_tagger_data as _get_tagger_data,
)

from .base import (
    BaseDriver as _BaseDriver
)

################################################################################################################################

class CkipTaggerWordSegmenter(_BaseDriver):  # pylint: disable=too-few-public-methods
    """The CKIP word-segmentation driver with CkipTagger backend."""

    def __init__(self):
        super().__init__()

        import ckiptagger
        self._core = ckiptagger.WS(_get_tagger_data())

    def __call__(self, *, text):
        assert isinstance(text, _TextParagraph)

        ws_list = self._core(text)
        ws = _SegParagraph.from_list(ws_list)

        return ws

class CkipTaggerPosTagger(_BaseDriver):  # pylint: disable=too-few-public-methods
    """The CKIP part-of-speech tagging driver with CkipTagger backend."""

    def __init__(self):
        super().__init__()

        import ckiptagger
        self._core = ckiptagger.POS(_get_tagger_data())

    def __call__(self, *, ws):
        assert isinstance(ws, _SegParagraph)

        pos_list = self._core(ws)
        pos = _SegParagraph.from_list(pos_list)

        return pos

class CkipTaggerNerChunker(_BaseDriver):  # pylint: disable=too-few-public-methods
    """The CKIP named-entity recognition driver with CkipTagger backend."""

    def __init__(self):
        super().__init__()

        import ckiptagger
        self._core = ckiptagger.NER(_get_tagger_data())

    def __call__(self, *, ws, pos):
        assert isinstance(ws, _SegParagraph)
        assert isinstance(pos, _SegParagraph)

        ner_list = self._core(ws, pos)
        ner = _NerParagraph.from_tagger(ner_list)

        return ner
