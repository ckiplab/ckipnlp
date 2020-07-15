#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides drivers with CkipClassic backend.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from itertools import (
    chain as _chain,
)

from ckipnlp.container import (
    TextParagraph as _TextParagraph,
    SegParagraph as _SegParagraph,
    WsPosSentence as _WsPosSentence,
    WsPosParagraph as _WsPosParagraph,
    ParsedParagraph as _ParsedParagraph,
)

from .base import (
    BaseDriver as _BaseDriver,
    DriverType as _DriverType,
    DriverFamily as _DriverFamily,
)

################################################################################################################################

class CkipClassicWordSegmenter(_BaseDriver):
    """The CKIP word segmentation driver with CkipClassic backend.

    Arguments
    ---------
        lazy : bool
            Lazy initialize underlying objects.
        do_pos : bool
            Returns POS-tag or not
        lexicons: Iterable[Tuple[str, str]]
            A list of the lexicon words and their POS-tags.

    .. method:: __call__(*, text)

        Apply word segmentation.

        Parameters
            **text** (:class:`TextParagraph <ckipnlp.container.text.TextParagraph>`) — The sentences.

        Returns
            - **ws** (:class:`TextParagraph <ckipnlp.container.text.TextParagraph>`) — The word-segmented sentences.
            - **pos** (:class:`TextParagraph <ckipnlp.container.text.TextParagraph>`) — The part-of-speech sentences.
              (returns if **do_pos** is set.)
    """

    driver_type = _DriverType.WORD_SEGMENTER
    driver_family = _DriverFamily.CLASSIC

    _count = 0

    def __init__(self, *, lazy=False, do_pos=False, lexicons=None):
        super().__init__(lazy=lazy)
        self._do_pos = do_pos
        self._lexicons = lexicons

    def _init(self):
        self.__class__._count += 1  # pylint: disable=protected-access
        if self.__class__._count > 1:  # pylint: disable=protected-access
            raise RuntimeError(f'Never instance more than one {self.__class__.__name__}!')

        import ckip_classic.ws
        self._core = ckip_classic.ws.CkipWs(
            new_style_format=True,
            lex_list=self._lexicons,
        )

    def _call(self, *, text):
        assert isinstance(text, _TextParagraph)

        wspos_text = self._core.apply_list(text.to_text())
        ws, pos = _WsPosParagraph.from_text(wspos_text)

        return (ws, pos,) if self._do_pos else ws

class CkipClassicSentenceParser(_BaseDriver):
    """The CKIP sentence parsing driver with CkipClassic backend.

    Arguments
    ---------
        lazy : bool
            Lazy initialize underlying objects.

    .. method:: __call__(*, ws, pos)

        Apply sentence parsing.

        Parameters
            - **ws** (:class:`TextParagraph <ckipnlp.container.text.TextParagraph>`) — The word-segmented sentences.
            - **pos** (:class:`TextParagraph <ckipnlp.container.text.TextParagraph>`) — The part-of-speech sentences.

        Returns
            **parsed** (:class:`ParsedSentence <ckipnlp.container.parsed.ParsedSentence>`) — The parsed-sentences.
    """

    driver_type = _DriverType.SENTENCE_PARSER
    driver_family = _DriverFamily.CLASSIC

    _count = 0

    def _init(self):
        self.__class__._count += 1  # pylint: disable=protected-access
        if self.__class__._count > 1:  # pylint: disable=protected-access
            raise RuntimeError(f'Never instance more than one {self.__class__.__name__}!')

        import ckip_classic.parser
        self._core = ckip_classic.parser.CkipParser(do_ws=False)

    def _call(self, *, ws, pos):
        assert isinstance(ws, _SegParagraph)
        assert isinstance(pos, _SegParagraph)


        parsed_text = []
        for ws_sent, pos_sent in zip(ws, pos):
            parsed_sent_text = []
            ws_clause = []
            pos_clause = []
            for ws_token, pos_token in _chain(zip(ws_sent, pos_sent), [(None, None),]):

                # Skip WHITESPACE
                if pos_token == 'WHITESPACE':
                    continue

                # Segment clauses by punctuations
                if pos_token is None or pos_token.endswith('CATEGORY'):
                    if ws_clause:
                        wspos_clause_text = _WsPosSentence.to_text(ws_clause, pos_clause)
                        for parsed_clause_text in self._core.apply_list([wspos_clause_text]):
                            parsed_sent_text.append([self._normalize(parsed_clause_text), '',])

                    if ws_token:
                        if not parsed_sent_text:
                            parsed_sent_text.append([None, '',])
                        parsed_sent_text[-1][1] += ws_token

                    ws_clause = []
                    pos_clause = []

                else:
                    ws_clause.append(self._half2full(ws_token))
                    pos_clause.append(pos_token)

            parsed_text.append(parsed_sent_text)
        parsed = _ParsedParagraph.from_list(parsed_text)

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

    @staticmethod
    def _normalize(text):
        return text.split('] ', 2)[-1].rstrip('#')
