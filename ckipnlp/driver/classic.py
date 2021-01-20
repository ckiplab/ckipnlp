#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides drivers with CkipClassic backend.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

from abc import (
    abstractmethod as _abstractmethod,
)

from itertools import (
    chain as _chain,
)

from ckipnlp.container import (
    TextParagraph as _TextParagraph,
    SegParagraph as _SegParagraph,
    WsPosSentence as _WsPosSentence,
    WsPosParagraph as _WsPosParagraph,
    ParseParagraph as _ParseParagraph,
)

from .base import (
    BaseDriver as _BaseDriver,
)

################################################################################################################################

class CkipClassicWordSegmenter(_BaseDriver):
    """The CKIP word segmentation driver with CkipClassic backend.

    Arguments
    ---------
        lazy : bool
            Lazy initialize the driver.
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

    driver_type = None
    driver_family = 'classic'
    driver_inputs = None

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

class _CkipClassicWordSegmenter(CkipClassicWordSegmenter):
    """The dummy class for :class:`CkipClassicWordSegmenter` for pipeline."""

    driver_type = 'word_segmenter'
    driver_family = 'classic'
    driver_inputs = ('text',)

    def __init__(self, *, lazy=False, lexicons=None):
        super().__init__(lazy=lazy, do_pos=False, lexicons=lexicons)

class _CkipClassic2WsPos(CkipClassicWordSegmenter):
    """The dummy class for :class:`CkipClassicWordSegmenter` for pipeline."""

    driver_type = '_wspos'
    driver_family = '_classic'
    driver_inputs = ('text',)

    def __init__(self, *, lazy=False, lexicons=None):
        super().__init__(lazy=lazy, do_pos=True, lexicons=lexicons)

class _CkipClassic2WordSegmenter(_BaseDriver):
    """The dummy class for :class:`CkipClassicWordSegmenter` for pipeline."""

    driver_type = 'word_segmenter'
    driver_family = '_classic'
    driver_inputs = ('_wspos',)

    def _init(self):
        pass

    def _call(self, *, _wspos):
        return _wspos[0]

class _CkipClassic2PosTagger(_BaseDriver):
    """The dummy class for :class:`CkipClassicWordSegmenter` for pipeline."""

    driver_type = 'pos_tagger'
    driver_family = '_classic'
    driver_inputs = ('_wspos',)

    def _init(self):
        pass

    def _call(self, *, _wspos):
        return _wspos[1]

################################################################################################################################

class _CkipClassicConParser(_BaseDriver):


    driver_type = 'con_parser'
    driver_inputs = ('ws', 'pos',)

    @_abstractmethod
    def driver_family(self):  # pylint: disable=missing-docstring
        return NotImplemented

    @_abstractmethod
    def _init(self):
        return NotImplemented

    def _call(self, *, ws, pos):
        assert isinstance(ws, _SegParagraph)
        assert isinstance(pos, _SegParagraph)


        conparse_text = []
        for ws_sent, pos_sent in zip(ws, pos):
            conparse_sent_text = []
            ws_clause = []
            pos_clause = []
            for ws_token, pos_token in _chain(zip(ws_sent, pos_sent), [(None, None),]):

                # Skip WHITESPACE
                if pos_token == 'WHITESPACE':
                    continue

                # Segment clauses by punctuations
                if pos_token is None or (pos_token.endswith('CATEGORY') and pos_token != 'PAUSECATEGORY'):
                    if ws_clause:
                        wspos_clause_text = _WsPosSentence.to_text(ws_clause, pos_clause)
                        for conparse_clause_text in self._core.apply_list([wspos_clause_text]):
                            conparse_sent_text.append([self._normalize(conparse_clause_text), '',])

                    if ws_token:
                        if not conparse_sent_text:
                            conparse_sent_text.append([None, '',])
                        conparse_sent_text[-1][1] += ws_token

                    ws_clause = []
                    pos_clause = []

                else:
                    ws_clause.append(self._half2full(ws_token))
                    pos_clause.append(pos_token)

            conparse_text.append(conparse_sent_text)
        conparse = _ParseParagraph.from_list(conparse_text)

        return conparse

    @staticmethod
    def _half2full(text):
        return text \
           .replace('(', '（') \
           .replace(')', '）') \
           .replace('+', '＋') \
           .replace('-', '－') \
           .replace(':', '：') \
           .replace('|', '｜')

    @staticmethod
    def _normalize(text):
        return text.split('] ', 2)[-1].rstrip('#')

################################################################################################################################

class CkipClassicConParser(_CkipClassicConParser):
    """The CKIP constituency parsing driver with CkipClassic backend.

    Arguments
    ---------
        lazy : bool
            Lazy initialize the driver.

    .. method:: __call__(*, ws, pos)

        Apply constituency parsing.

        Parameters
            - **ws** (:class:`~ckipnlp.container.text.TextParagraph`) — The word-segmented sentences.
            - **pos** (:class:`~ckipnlp.container.text.TextParagraph`) — The part-of-speech sentences.

        Returns
            **conparse** (:class:`~ckipnlp.container.parse.ParseSentence`) — The constituency-parsing sentences.
    """

    driver_family = 'classic'

    _count = 0

    def _init(self):

        self.__class__._count += 1  # pylint: disable=protected-access
        if self.__class__._count > 1:  # pylint: disable=protected-access
            raise RuntimeError(f'Never instance more than one {self.__class__.__name__}!')

        import ckip_classic.parser
        self._core = ckip_classic.parser.CkipParser(do_ws=False)

class CkipClassicConParserClient(_CkipClassicConParser):
    """The CKIP constituency parsing driver with CkipClassic client backend.

    Arguments
    ---------
        lazy : bool
            Lazy initialize the driver.

    Notes
    -----

        Please register an account at http://parser.iis.sinica.edu.tw/v1/reg.exe and
        set the environment variables ``$CKIPPARSER_USERNAME`` and ``$CKIPPARSER_PASSWORD``.

    .. method:: __call__(*, ws, pos)

        Apply constituency parsing.

        Parameters
            - **ws** (:class:`~ckipnlp.container.text.TextParagraph`) — The word-segmented sentences.
            - **pos** (:class:`~ckipnlp.container.text.TextParagraph`) — The part-of-speech sentences.

        Returns
            **conparse** (:class:`~ckipnlp.container.parse.ParseSentence`) — The constituency-parsing sentences.

    """

    driver_family = 'classic-client'

    def _init(self):

        import ckip_classic.client
        self._core = ckip_classic.client.CkipParserClient()
