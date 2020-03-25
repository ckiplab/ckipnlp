#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

# import ckiptagger

from ckipnlp.container import (
    TextSentenceList as _TextSentenceList,
    SegSentenceList as _SegSentenceList,
    WsSentenceList as _WsSentenceList,
    NerSentenceList as _NerSentenceList,
)

from .base import (
    BaseDriver as _BaseDriver
)

################################################################################################################################

class CkipTaggerSeg(_BaseDriver):
    """The CKIP word segmentation driver with tagger backend."""

    def __call__(self, *, text):
        assert isinstance(text, _TextSentenceList)
        return _SegSentenceList()

class CkipTaggerPos(_BaseDriver):
    """The CKIP part-of-speech tagging driver with tagger backend."""

    def __call__(self, *, seg):
        assert isinstance(seg, _SegSentenceList)
        return _WsSentenceList()

class CkipTaggerNer(_BaseDriver):
    """The CKIP named entity recognition driver with tagger backend."""

    def __call__(self, *, ws):
        assert isinstance(ws, _WsSentenceList)
        return _NerSentenceList()
