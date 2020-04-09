#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from ckipnlp.driver import (
    DriverType as _DriverType,
    CkipClassicWordSegmenter as _CkipClassicWordSegmenter,
    CkipClassicSentenceParser as _CkipClassicSentenceParser,
    CkipTaggerWordSegmenter as _CkipTaggerWordSegmenter,
    CkipTaggerPosTagger as _CkipTaggerPosTagger,
    CkipTaggerNerChunker as _CkipTaggerNerChunker,
    CkipNaiveSentenceSegmenter as _CkipNaiveSentenceSegmenter,
)

################################################################################################################################

class CkipCoreDocument:  # pylint: disable=too-few-public-methods
    """The core document.

    Attributes
    ----------
        raw
            *str* – The unsegmented text input.
        text
            :class:`TextParagraph` – The sentences.
        ws
            :class:`SegParagraph` – The word-segmented sentences.
        pos
            :class:`SegParagraph` – The part-of-speech sentences.
        ner
            :class:`NerParagraph` – The named-entity recognition results.
        parsed
            :class:`ParsedParagraph` – The parsed-sentences.
    """

    def __init__(self, *, raw=None, text=None, ws=None, pos=None, ner=None, parsed=None):
        self.raw = raw
        self.text = text
        self.ws = ws
        self.pos = pos
        self.ner = ner
        self.parsed = parsed

        self._wspos = None

################################################################################################################################

class CkipCorePipeline:  # pylint: disable=too-few-public-methods
    """The core pipeline.

    Arguments
    ---------
        sentence_segmenter_type : :class:`DriverType`
            The type of sentence-segmenter. (`DriverType.NAIVE`)

        word_segmenter_type : :class:`DriverType`
            The type of word-segmenter. (`DriverType.TAGGER`, `DriverType.CLASSIC`)

        pos_tagger_type : :class:`DriverType`
            The type of part-of-speech tagger. (`DriverType.TAGGER`, `DriverType.CLASSIC`)

        ner_chunker_type : :class:`DriverType`
            The type of named-entity recognition chunker. (`DriverType.TAGGER`)

        sentence_parser_type : :class:`DriverType`
            The type of named-entity recognition chunker. (`DriverType.CLASSIC`)

    """

    def __init__(self, *,
            sentence_segmenter_type=None,
            word_segmenter_type=None,
            pos_tagger_type=None,
            ner_chunker_type=None,
            sentence_parser_type=None,
        ):

        self._sentence_segmenter = None
        self._word_segmenter = None
        self._pos_tagger = None
        self._wspos_driver = None
        self._ner_chunker = None
        self._sentence_parser = None

        # Punctuation
        if sentence_segmenter_type is None:
            pass
        elif sentence_segmenter_type is _DriverType.NAIVE:
            self._sentence_segmenter = _CkipNaiveSentenceSegmenter()
        else:
            raise KeyError(f'Sentence segmentation is not implemented for type {sentence_segmenter_type.name}')

        # WS
        if word_segmenter_type is None:
            pass
        elif word_segmenter_type == _DriverType.TAGGER:
            self._word_segmenter = _CkipTaggerWordSegmenter()
        elif word_segmenter_type == _DriverType.CLASSIC:
            if pos_tagger_type == _DriverType.CLASSIC:
                self._wspos_driver = _CkipClassicWordSegmenter(do_pos=True)
                pos_tagger_type = None
            else:
                self._word_segmenter = _CkipClassicWordSegmenter()
        else:
            raise KeyError(f'Word segmentation is not implemented for type {word_segmenter_type.name}')

        # POS
        if pos_tagger_type is None:
            pass
        elif pos_tagger_type == _DriverType.TAGGER:
            self._pos_tagger = _CkipTaggerPosTagger()
        else:
            raise KeyError(f'Part-of-speech tagging is not implemented for type {pos_tagger_type.name}')

        # NER
        if ner_chunker_type is None:
            pass
        elif ner_chunker_type == _DriverType.TAGGER:
            self._ner_chunker = _CkipTaggerNerChunker()
        else:
            raise KeyError(f'Named entity recognition is not implemented for type {ner_chunker_type.name}')

        # Parser
        if sentence_parser_type is None:
            pass
        elif sentence_parser_type == _DriverType.CLASSIC:
            self._sentence_parser = _CkipClassicSentenceParser()
        else:
            raise KeyError(f'Sentence parsing is not implemented for type {sentence_parser_type.name}')

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
                text=self.sentence_segment(doc)
            )

        return doc._wspos  # pylint: disable=protected-access

    ########################################################################################################################

    def sentence_segment(self, doc):
        """Apply sentence segmentation.

        Arguments
        ---------
            doc : :class:`CkipCoreDocument`
                The input document.

        Returns
        -------
            doc.text : :class:`TextParagraph`
                The sentences.

        .. note::

            This routine modify **doc** inplace.
        """
        if doc.text is None:

            if self._sentence_segmenter is not None:
                doc.text = self._sentence_segmenter(
                    raw=self._get_raw(doc)
                )

            else:
                raise AttributeError('No sentence-segmentation driver / No valid text input!')

        return doc.text

    ########################################################################################################################

    def word_segment(self, doc):
        """Apply word segmentation.

        Arguments
        ---------
            doc : :class:`CkipCoreDocument`
                The input document.

        Returns
        -------
            doc.ws : :class:`SegParagraph`
                The word-segmented sentences.

        .. note::

            This routine modify **doc** inplace.
        """
        if doc.ws is None:

            if self._word_segmenter is not None:
                doc.ws = self._word_segmenter(
                    text=self.sentence_segment(doc)
                )

            elif self._wspos_driver is not None:
                doc.ws, _ = self._get_wspos(doc)

            else:
                raise AttributeError('No word-segmentation driver / No valid word-segmentation input!')

        return doc.ws

    ########################################################################################################################

    def pos_tag(self, doc):
        """Apply part-of-speech tagging.

        Arguments
        ---------
            doc : :class:`CkipCoreDocument`
                The input document.

        Returns
        -------
            doc.pos : :class:`SegParagraph`
                The part-of-speech sentences.

        .. note::

            This routine modify **doc** inplace.
        """
        if doc.pos is None:

            if self._pos_tagger is not None:
                doc.pos = self._pos_tagger(
                    ws=self.word_segment(doc)
                )

            elif self._wspos_driver is not None:
                _, doc.pos = self._get_wspos(doc)

            else:
                raise AttributeError('No part-of-speech tagging driver / No valid part-of-speech tagging input!')

        return doc.pos

    ########################################################################################################################

    def ner_chunk(self, doc):
        """Apply named-entity recognition.

        Arguments
        ---------
            doc : :class:`CkipCoreDocument`
                The input document.

        Returns
        -------
            doc.ner : :class:`NerParagraph`
                The named-entity recognition results.

        .. note::

            This routine modify **doc** inplace.
        """
        if doc.ner is None:

            if self._ner_chunker is not None:
                doc.ner = self._ner_chunker(
                    ws=self.word_segment(doc),
                    pos=self.pos_tag(doc),
                )

            else:
                raise AttributeError('No named-entity recognition driver / No valid named-entity recognition input!')

        return doc.ner

    ########################################################################################################################

    def sentence_parse(self, doc):
        """Apply sentence parsing.

        Arguments
        ---------
            doc : :class:`CkipCoreDocument`
                The input document.

        Returns
        -------
            doc.parsed : :class:`ParsedParagraph`
                The parsed sentences.

        .. note::

            This routine modify **doc** inplace.
        """
        if doc.parsed is None:

            if self._sentence_parser is not None:
                doc.parsed = self._sentence_parser(
                    ws=self.word_segment(doc),
                    pos=self.pos_tag(doc),
                )

            else:
                raise AttributeError('No sentence parsing driver / No valid sentence parsing input!')

        return doc.parsed
