#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from ckipnlp.container import (
    TextSentenceList as _TextSentenceList,
    WsSentenceList as _WsSentenceList,
    ParsedSentenceList as _ParsedSentenceList,
)

from .base import (
    BaseDriver as _BaseDriver
)

################################################################################################################################

class CkipClassicWs(_BaseDriver):  # pylint: disable=too-few-public-methods
    """The CKIP word segmentation driver with classic backend."""

    def __init__(self):
        super().__init__()

        import ckip_classic.ws
        self._core = ckip_classic.ws.CkipWs()

    def __call__(self, *, text):
        assert isinstance(text, _TextSentenceList)

        ws_text = self._core.apply_list(text.to_text())
        ws = _WsSentenceList.from_text(ws_text)

        return ws

class CkipClassicParser(_BaseDriver):  # pylint: disable=too-few-public-methods
    """The CKIP sentence parsing driver with classic backend."""

    def __init__(self):
        super().__init__()

        import ckip_classic.parser
        self._core = ckip_classic.parser.CkipParser(do_ws=False)

    def __call__(self, *, ws):
        assert isinstance(ws, _WsSentenceList)

        ws_text = ws.to_text()
        parsed_text = self._core.apply_list(ws_text)
        parsed = _ParsedSentenceList.from_text(parsed_text)

        return parsed
