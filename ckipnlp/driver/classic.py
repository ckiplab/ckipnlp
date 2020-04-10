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
    DriverType as _DriverType,
    DriverKind as _DriverKind,
)

################################################################################################################################

class CkipClassicWordSegmenter(_BaseDriver,  # pylint: disable=too-few-public-methods
    driver_type=_DriverType.WORD_SEGMENTER,
    driver_kind=_DriverKind.CLASSIC,
):
    """The CKIP word segmentation driver with CkipClassic backend."""

    _count = 0

    def __init__(self, *, do_pos=False, init=True):
        super().__init__(init=init)
        self._do_pos = do_pos

    def _init(self):
        if self.__class__._count >= 1:
            raise RuntimeError(f'Never instance more than one {self.__class__.__name__}!')
        self.__class__._count += 1

        import ckip_classic.ws
        self._core = ckip_classic.ws.CkipWs()

    def _call(self, *, text):
        assert isinstance(text, _TextParagraph)

        wspos_text = self._core.apply_list(text.to_text())
        ws, pos = _WsPosParagraph.from_text(wspos_text)

        return ws, pos if self._do_pos else ws

class CkipClassicSentenceParser(_BaseDriver,  # pylint: disable=too-few-public-methods
    driver_type=_DriverType.SENTENCE_PARSER,
    driver_kind=_DriverKind.CLASSIC,
):
    """The CKIP sentence parsing driver with CkipClassic backend."""

    _count = 0

    def _init(self):
        super()._init()

        if self.__class__._count >= 1:
            raise RuntimeError(f'Never instance more than one {self.__class__.__name__}!')
        self.__class__._count += 1

        import ckip_classic.parser
        self._core = ckip_classic.parser.CkipParser(do_ws=False)

    def _call(self, *, ws, pos):
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
