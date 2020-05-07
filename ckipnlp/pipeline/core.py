#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides core CKIPNLP pipeline.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from collections.abc import (
    Mapping as _Mapping,
)

from ckipnlp.driver.base import (
    DriverType as _DriverType,
    DriverFamily as _DriverFamily,
    DriverRegister as _DriverRegister,
)

###############################################################################################################################)

class CkipDocument(_Mapping):
    """The core document.

    Attributes
    ----------
        raw : str
            The unsegmented text input.
        text : :class:`TextParagraph <ckipnlp.container.text.TextParagraph>`
            The sentences.
        ws : :class:`SegParagraph <ckipnlp.container.seg.SegParagraph>`
            The word-segmented sentences.
        pos : :class:`SegParagraph <ckipnlp.container.seg.SegParagraph>`
            The part-of-speech sentences.
        ner : :class:`NerParagraph <ckipnlp.container.ner.NerParagraph>`
            The named-entity recognition results.
        parsed : :class:`ParsedParagraph <ckipnlp.container.parsed.ParsedParagraph>`
            The parsed-sentences.
    """

    __keys = ('raw', 'text', 'ws', 'pos', 'ner', 'parsed',)

    def __init__(self, *, raw=None, text=None, ws=None, pos=None, ner=None, parsed=None):
        self.raw = raw
        self.text = text
        self.ws = ws
        self.pos = pos
        self.ner = ner
        self.parsed = parsed

        self._wspos = None

    def __len__(self):
        return len(self.__keys)

    def __iter__(self):
        yield from self.__keys

    def __getitem__(self, key):
        return getattr(self, key)

################################################################################################################################

class CkipPipeline:
    """The core pipeline.

    Arguments
    ---------
        sentence_segmenter : :class:`DriverFamily <ckipnlp.driver.base.DriverFamily>`
            The type of sentence segmenter.

        word_segmenter : :class:`DriverFamily <ckipnlp.driver.base.DriverFamily>`
            The type of word segmenter.

        pos_tagger : :class:`DriverFamily <ckipnlp.driver.base.DriverFamily>`
            The type of part-of-speech tagger.

        ner_chunker : :class:`DriverFamily <ckipnlp.driver.base.DriverFamily>`
            The type of named-entity recognition chunker.

        sentence_parser : :class:`DriverFamily <ckipnlp.driver.base.DriverFamily>`
            The type of sentence parser.

    Other Parameters
    ----------------
        lazy : bool
            Lazy initialize the drivers.

        opts : Dict[str, Dict]
            The driver options. Key: driver name (e.g. `'sentence_segmenter'`); Value: a dictionary of options.
    """

    def __init__(self, *,
            sentence_segmenter=_DriverFamily.BUILTIN,
            word_segmenter=_DriverFamily.TAGGER,
            pos_tagger=_DriverFamily.TAGGER,
            sentence_parser=_DriverFamily.CLASSIC,
            ner_chunker=_DriverFamily.TAGGER,
            lazy=True,
            opts={},
        ):

        # WS & POS
        if word_segmenter == _DriverFamily.CLASSIC and pos_tagger == _DriverFamily.CLASSIC:
            self._wspos_driver = _DriverRegister.get(_DriverType.WORD_SEGMENTER, _DriverFamily.CLASSIC)(
                do_pos=True, lazy=lazy, **opts.get('word_segmenter', {}), **opts.get('pos_tagger', {}),
            )
            word_segmenter = None
            pos_tagger = None
        else:
            self._wspos_driver = _DriverRegister.get(None, None)(
                lazy=lazy, **opts.get('word_segmenter', {}),
            )

        self._sentence_segmenter = _DriverRegister.get(_DriverType.SENTENCE_SEGMENTER, sentence_segmenter)(
            lazy=lazy, **opts.get('sentence_segmenter', {}),
        )
        self._word_segmenter = _DriverRegister.get(_DriverType.WORD_SEGMENTER, word_segmenter)(
            lazy=lazy, **opts.get('word_segmenter', {}),
        )
        self._pos_tagger = _DriverRegister.get(_DriverType.POS_TAGGER, pos_tagger)(
            lazy=lazy, **opts.get('pos_tagger', {}),
        )
        self._sentence_parser = _DriverRegister.get(_DriverType.SENTENCE_PARSER, sentence_parser)(
            lazy=lazy, **opts.get('sentence_parser', {}),
        )
        self._ner_chunker = _DriverRegister.get(_DriverType.NER_CHUNKER, ner_chunker)(
            lazy=lazy, **opts.get('ner_chunker', {}),
        )

    ########################################################################################################################

    @staticmethod
    def _get_raw(doc):
        if doc.raw is None:
            raise AttributeError('No raw text!')
        return doc.raw

    ########################################################################################################################

    def _get_wspos(self, doc):
        if doc._wspos is None:  # pylint: disable=protected-access

            doc._wspos = self._wspos_driver(  # pylint: disable=protected-access
                text=self.get_text(doc)
            )

        return doc._wspos  # pylint: disable=protected-access

    ########################################################################################################################

    def get_text(self, doc):
        """Apply sentence segmentation.

        Arguments
        ---------
            doc : :class:`CkipDocument`
                The input document.

        Returns
        -------
            doc.text : :class:`TextParagraph <ckipnlp.container.text.TextParagraph>`
                The sentences.

        .. note::

            This routine modify **doc** inplace.
        """
        if doc.text is None:

            if not self._sentence_segmenter.is_dummy:
                doc.text = self._sentence_segmenter(
                    raw=self._get_raw(doc)
                )

            else:
                raise AttributeError('No sentence segmentation driver / No valid text input!')

        return doc.text

    ########################################################################################################################

    def get_ws(self, doc):
        """Apply word segmentation.

        Arguments
        ---------
            doc : :class:`CkipDocument`
                The input document.

        Returns
        -------
            doc.ws : :class:`SegParagraph <ckipnlp.container.seg.SegParagraph>`
                The word-segmented sentences.

        .. note::

            This routine modify **doc** inplace.
        """
        if doc.ws is None:

            if not self._word_segmenter.is_dummy:
                doc.ws = self._word_segmenter(
                    text=self.get_text(doc)
                )

            elif not self._wspos_driver.is_dummy:
                doc.ws, _ = self._get_wspos(doc)

            else:
                raise AttributeError('No word segmentation driver / No valid word segmentation input!')

        return doc.ws

    ########################################################################################################################

    def get_pos(self, doc):
        """Apply part-of-speech tagging.

        Arguments
        ---------
            doc : :class:`CkipDocument`
                The input document.

        Returns
        -------
            doc.pos : :class:`SegParagraph <ckipnlp.container.seg.SegParagraph>`
                The part-of-speech sentences.

        .. note::

            This routine modify **doc** inplace.
        """
        if doc.pos is None:

            if not self._pos_tagger.is_dummy:
                doc.pos = self._pos_tagger(
                    ws=self.get_ws(doc)
                )

            elif not self._wspos_driver.is_dummy:
                _, doc.pos = self._get_wspos(doc)

            else:
                raise AttributeError('No part-of-speech tagging driver / No valid part-of-speech tagging input!')

        return doc.pos

    ########################################################################################################################

    def get_ner(self, doc):
        """Apply named-entity recognition.

        Arguments
        ---------
            doc : :class:`CkipDocument`
                The input document.

        Returns
        -------
            doc.ner : :class:`NerParagraph <ckipnlp.container.ner.NerParagraph>`
                The named-entity recognition results.

        .. note::

            This routine modify **doc** inplace.
        """
        if doc.ner is None:

            if not self._ner_chunker.is_dummy:
                doc.ner = self._ner_chunker(
                    ws=self.get_ws(doc),
                    pos=self.get_pos(doc),
                )

            else:
                raise AttributeError('No named-entity recognition driver / No valid named-entity recognition input!')

        return doc.ner

    ########################################################################################################################

    def get_parsed(self, doc):
        """Apply sentence parsing.

        Arguments
        ---------
            doc : :class:`CkipDocument`
                The input document.

        Returns
        -------
            doc.parsed : :class:`ParsedParagraph <ckipnlp.container.parsed.ParsedParagraph>`
                The parsed sentences.

        .. note::

            This routine modify **doc** inplace.
        """
        if doc.parsed is None:

            if not self._sentence_parser.is_dummy:
                doc.parsed = self._sentence_parser(
                    ws=self.get_ws(doc),
                    pos=self.get_pos(doc),
                )

            else:
                raise AttributeError('No sentence parsing driver / No valid sentence parsing input!')

        return doc.parsed
