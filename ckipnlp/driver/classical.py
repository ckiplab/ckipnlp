#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from ckipnlp.container import (
    TextSentenceList as _TextSentenceList,
    WsSentenceList as _WsSentenceList,
    ParseSentenceList as _ParseSentenceList,
)

from .base import (
    BaseDriver as _BaseDriver
)

################################################################################################################################

class CkipClassicalWs(_BaseDriver):
    """The CKIP word segmentation driver with classical backend."""

    def __call__(self, *, text):
        assert isinstance(text, _TextSentenceList)
        return _WsSentenceList()

class CkipClassicalParser(_BaseDriver):
    """The CKIP sentence parsing driver with classical backend."""

    def __call__(self, *, ws):
        assert isinstance(ws, _WsSentenceList)
        return _ParseSentenceList()
