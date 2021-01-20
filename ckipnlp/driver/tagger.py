#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides drivers with CkipTagger backend.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

from ckipnlp.container import (
    TextParagraph as _TextParagraph,
    SegParagraph as _SegParagraph,
    NerParagraph as _NerParagraph,
)

from ckipnlp.util.data import (
    get_tagger_data as _get_tagger_data,
)

from .base import (
    BaseDriver as _BaseDriver,
)

################################################################################################################################

class CkipTaggerWordSegmenter(_BaseDriver):
    """The CKIP word segmentation driver with CkipTagger backend.

    Arguments
    ---------
        lazy : bool
            Lazy initialize the driver.
        disable_cuda : bool
            Disable GPU usage.
        recommend_lexicons: Mapping[str, float]
            A mapping of lexicon words to their relative weights.
        coerce_lexicons: Mapping[str, float]
            A mapping of lexicon words to their relative weights.

    Other Parameters
    ----------------
        **opts
            Extra options for :meth:`ckiptagger.WS.__call__`.
            (Please refer https://github.com/ckiplab/ckiptagger#4-run-the-ws-pos-ner-pipeline for details.)


    .. method:: __call__(*, text)

        Apply word segmentation.

        Parameters
            **text** (:class:`TextParagraph <ckipnlp.container.text.TextParagraph>`) — The sentences.

        Returns
            **ws** (:class:`TextParagraph <ckipnlp.container.text.TextParagraph>`) — The word-segmented sentences.
    """

    driver_type = 'word_segmenter'
    driver_family = 'tagger'
    driver_inputs = ('text',)

    def __init__(self, *, lazy=False, disable_cuda=True, recommend_lexicons={}, coerce_lexicons={}, **opts):
        super().__init__(lazy=lazy)
        self._disable_cuda = disable_cuda
        self._recommend_lexicons = recommend_lexicons
        self._coerce_lexicons = coerce_lexicons
        self._opts = opts

    def _init(self):
        import ckiptagger

        if self._recommend_lexicons:
            self._opts['recommend_dictionary'] = ckiptagger.construct_dictionary(self._recommend_lexicons)
        if self._coerce_lexicons:
            self._opts['coerce_dictionary'] = ckiptagger.construct_dictionary(self._coerce_lexicons)

        self._core = ckiptagger.WS(_get_tagger_data(), disable_cuda=self._disable_cuda)

    def _call(self, *, text):
        assert isinstance(text, _TextParagraph)

        ws_list = self._core(text, **self._opts)
        ws = _SegParagraph.from_list(ws_list)

        return ws

################################################################################################################################

class CkipTaggerPosTagger(_BaseDriver):
    """The CKIP part-of-speech tagging driver with CkipTagger backend.

    Arguments
    ---------
        lazy : bool
            Lazy initialize the driver.
        disable_cuda : bool
            Disable GPU usage.

    Other Parameters
    ----------------
        **opts
            Extra options for :meth:`ckiptagger.POS.__call__`.
            (Please refer https://github.com/ckiplab/ckiptagger#4-run-the-ws-pos-ner-pipeline for details.)

    .. method:: __call__(*, text)

        Apply part-of-speech tagging.

        Parameters
            **ws** (:class:`TextParagraph <ckipnlp.container.text.TextParagraph>`) — The word-segmented sentences.

        Returns
            **pos** (:class:`TextParagraph <ckipnlp.container.text.TextParagraph>`) — The part-of-speech sentences.
    """

    driver_type = 'pos_tagger'
    driver_family = 'tagger'
    driver_inputs = ('ws',)

    def __init__(self, *, lazy=False, disable_cuda=True, **opts):
        super().__init__(lazy=lazy)
        self._disable_cuda = disable_cuda
        self._opts = opts

    def _init(self):
        import ckiptagger
        self._core = ckiptagger.POS(_get_tagger_data(), disable_cuda=self._disable_cuda)

    def _call(self, *, ws):
        assert isinstance(ws, _SegParagraph)

        pos_list = self._core(ws, **self._opts)
        pos = _SegParagraph.from_list(pos_list)

        return pos

################################################################################################################################

class CkipTaggerNerChunker(_BaseDriver):
    """The CKIP named-entity recognition driver with CkipTagger backend.

    Arguments
    ---------
        lazy : bool
            Lazy initialize the driver.
        disable_cuda : bool
            Disable GPU usage.

    Other Parameters
    ----------------
        **opts
            Extra options for :meth:`ckiptagger.NER.__call__`.
            (Please refer https://github.com/ckiplab/ckiptagger#4-run-the-ws-pos-ner-pipeline for details.)

    .. method:: __call__(*, text)

        Apply named-entity recognition.

        Parameters
            - **ws** (:class:`TextParagraph <ckipnlp.container.text.TextParagraph>`) — The word-segmented sentences.
            - **pos** (:class:`TextParagraph <ckipnlp.container.text.TextParagraph>`) — The part-of-speech sentences.

        Returns
            **ner** (:class:`NerParagraph <ckipnlp.container.ner.NerParagraph>`) — The named-entity recognition results.
    """

    driver_type = 'ner_tagger'
    driver_family = 'tagger'
    driver_inputs = ('ws', 'pos',)

    def __init__(self, *, lazy=False, disable_cuda=True, **opts):
        super().__init__(lazy=lazy)
        self._disable_cuda = disable_cuda
        self._opts = opts

    def _init(self):
        import ckiptagger
        self._core = ckiptagger.NER(_get_tagger_data(), disable_cuda=self._disable_cuda)

    def _call(self, *, ws, pos):
        assert isinstance(ws, _SegParagraph)
        assert isinstance(pos, _SegParagraph)

        ner_list = self._core(ws, pos, **self._opts)
        ner = _NerParagraph.from_tagger(ner_list)

        return ner
