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

class CkipClassicWs(_BaseDriver):  # pylint: disable=too-few-public-methods
    """The CKIP word segmentation driver with classic backend."""

    def __init__(self):
        super().__init__()
        # self._core = CkipWsWrapper()
        self._core = None

    def __call__(self, *, text):
        assert isinstance(text, _TextSentenceList)

        ws_text = self._core.apply_list(text)
        ws = _WsSentenceList.from_text(ws_text)

        return ws

class CkipClassicParser(_BaseDriver):  # pylint: disable=too-few-public-methods
    """The CKIP sentence parsing driver with classic backend."""

    def __init__(self):
        super().__init__()
        # self._core = CkipParserWrapper()
        self._core = None

    def __call__(self, *, ws):
        assert isinstance(ws, _WsSentenceList)
        return _ParseSentenceList()
