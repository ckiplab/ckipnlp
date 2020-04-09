#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from ckipnlp.container import (
    TextParagraph as _TextParagraph,
    SegParagraph as _SegParagraph,
    WsPosParagraph as _WsPosParagraph,
    ParsedParagraph as _ParsedParagraph,
)

from .base import (
    BaseDriver as _BaseDriver,
)

################################################################################################################################

class CkipClassicWordSegmenter(_BaseDriver):  # pylint: disable=too-few-public-methods
    """The CKIP word-segmentation driver with CkipClassic backend."""

    def __init__(self, *, do_pos=False):
        super().__init__()

        import ckip_classic.ws
        self._core = ckip_classic.ws.CkipWs()
        self._do_pos = do_pos

    def __call__(self, *, text):
        assert isinstance(text, _TextParagraph)

        wspos_text = self._core.apply_list(text.to_text())
        ws, pos = _WsPosParagraph.from_text(wspos_text)

        return ws, pos if self._do_pos else ws

class CkipClassicSentenceParser(_BaseDriver):  # pylint: disable=too-few-public-methods
    """The CKIP sentence parsing driver with CkipClassic backend."""

    def __init__(self):
        super().__init__()

        import ckip_classic.parser
        self._core = ckip_classic.parser.CkipParser(do_ws=False)

    def __call__(self, *, ws, pos):
        assert isinstance(ws, _SegParagraph)
        assert isinstance(pos, _SegParagraph)

        ws_text = _WsPosParagraph.to_text(ws, pos)
        parsed_text = self._core.apply_list(ws_text)
        parsed = _ParsedParagraph.from_text(parsed_text)

        return parsed

    @staticmethod
    def _half2full(text):
        return text \
           .replace('(', '（') \
           .replace(')', '）') \
           .replace('+', '＋') \
           .replace('-', '－') \
           .replace(':', '：') \
           .replace('|', '｜') \
           .replace('&', '＆') \
           .replace('#', '＃')
