#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides kernel CKIPNLP pipeline.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

from collections.abc import (
    Mapping as _Mapping,
)

from ckipnlp.driver.base import (
    DriverRegister as _DriverRegister,
)

###############################################################################################################################)

class CkipDocument(_Mapping):
    """The kernel document.

    Attributes
    ----------
        raw : str
            The unsegmented text input.
        text : :class:`~ckipnlp.container.text.TextParagraph`
            The sentences.
        ws : :class:`~ckipnlp.container.seg.SegParagraph`
            The word-segmented sentences.
        pos : :class:`~ckipnlp.container.seg.SegParagraph`
            The part-of-speech sentences.
        ner : :class:`~ckipnlp.container.ner.NerParagraph`
            The named-entity recognition results.
        conparse : :class:`~ckipnlp.container.parse.ParseParagraph`
            The constituency-parsing sentences.
    """

    __keys = ('raw', 'text', 'ws', 'pos', 'ner', 'conparse',)

    def __init__(self, *, raw=None, text=None, ws=None, pos=None, ner=None, conparse=None):
        self.raw = raw
        self.text = text
        self.ws = ws
        self.pos = pos
        self.ner = ner
        self.conparse = conparse

        self._wspos = None

    def __len__(self):
        return len(self.__keys)

    def __iter__(self):
        yield from self.__keys

    def __getitem__(self, key):
        return getattr(self, key)

################################################################################################################################

class CkipPipeline:
    """The kernel pipeline.

    Arguments
    ---------
        sentence_segmenter : str
            The type of sentence segmenter.

        word_segmenter : str
            The type of word segmenter.

        pos_tagger : str
            The type of part-of-speech tagger.

        ner_chunker : str
            The type of named-entity recognition chunker.

        con_parser : str
            The type of constituency parser.

    Other Parameters
    ----------------
        lazy : bool
            Lazy initialize the drivers.

        opts : Dict[str, Dict]
            The driver options. Key: driver name (e.g. `'sentence_segmenter'`); Value: a dictionary of options.
    """

    def __init__(self, *,
            sentence_segmenter='default',
            word_segmenter='tagger',
            pos_tagger='tagger',
            con_parser='classic-client',
            ner_chunker='tagger',
            lazy=True,
            opts={},
        ):

        if word_segmenter == '_classic':
            word_segmenter = 'classic'
        if pos_tagger == '_classic':
            pos_tagger = 'classic'

        # WS & POS
        if pos_tagger == 'classic':
            assert word_segmenter == 'classic', 'CkipClassicPosTagger must be used with CkipClassicWordSegmenter together!'
            self._wspos_driver = _DriverRegister.get('_wspos', '_classic')(
                lazy=lazy, **opts.get('word_segmenter', {}), **opts.get('pos_tagger', {}),
            )
            word_segmenter = '_classic'
            pos_tagger = '_classic'
        else:
            self._wspos_driver = _DriverRegister.get(None, None)()

        self._sentence_segmenter = _DriverRegister.get('sentence_segmenter', sentence_segmenter)(
            lazy=lazy, **opts.get('sentence_segmenter', {}),
        )
        self._word_segmenter = _DriverRegister.get('word_segmenter', word_segmenter)(
            lazy=lazy, **opts.get('word_segmenter', {}),
        )
        self._pos_tagger = _DriverRegister.get('pos_tagger', pos_tagger)(
            lazy=lazy, **opts.get('pos_tagger', {}),
        )
        self._con_parser = _DriverRegister.get('con_parser', con_parser)(
            lazy=lazy, **opts.get('con_parser', {}),
        )
        self._ner_chunker = _DriverRegister.get('ner_tagger', ner_chunker)(
            lazy=lazy, **opts.get('ner_chunker', {}),
        )

    ########################################################################################################################

    def _get(self, key, doc):
        driver, name = {
            'raw': (
                None, None,
            ),
            '_wspos': (
                self._wspos_driver, 'classic word segmentation',
            ),
            'text': (
                self._sentence_segmenter, 'sentence segmentation',
            ),
            'ws': (
                self._word_segmenter, 'word segmentation',
            ),
            'pos': (
                self._pos_tagger, 'part-of-speech tagging',
            ),
            'conparse': (
                self._con_parser, 'constituency parsing',
            ),
            'ner': (
                self._ner_chunker, 'named-entity recognition',
            ),
        }[key]

        if doc[key] is NotImplemented:
            raise RecursionError('Loop dependence detected!')

        if doc[key] is None:
            setattr(doc, key, NotImplemented)

            if key == 'raw':
                raise AttributeError('No raw text!')
            elif not driver.is_dummy:
                ret = driver._call_from_pipeline(self, doc)  # pylint: disable=protected-access
                setattr(doc, key, ret)
            else:
                raise AttributeError(f'No {name} driver / no {name} as input!')

        return doc[key]

    ########################################################################################################################

    def get_text(self, doc):
        """Apply sentence segmentation.

        Arguments
        ---------
            doc : :class:`CkipDocument`
                The input document.

        Returns
        -------
            doc.text : :class:`~ckipnlp.container.text.TextParagraph`
                The sentences.

        .. note::

            This routine modify **doc** inplace.
        """
        return self._get('text', doc)

    ########################################################################################################################

    def get_ws(self, doc):
        """Apply word segmentation.

        Arguments
        ---------
            doc : :class:`CkipDocument`
                The input document.

        Returns
        -------
            doc.ws : :class:`~ckipnlp.container.seg.SegParagraph`
                The word-segmented sentences.

        .. note::

            This routine modify **doc** inplace.
        """
        return self._get('ws', doc)

    ########################################################################################################################

    def get_pos(self, doc):
        """Apply part-of-speech tagging.

        Arguments
        ---------
            doc : :class:`CkipDocument`
                The input document.

        Returns
        -------
            doc.pos : :class:`~ckipnlp.container.seg.SegParagraph`
                The part-of-speech sentences.

        .. note::

            This routine modify **doc** inplace.
        """
        return self._get('pos', doc)

    ########################################################################################################################

    def get_ner(self, doc):
        """Apply named-entity recognition.

        Arguments
        ---------
            doc : :class:`CkipDocument`
                The input document.

        Returns
        -------
            doc.ner : :class:`~ckipnlp.container.ner.NerParagraph`
                The named-entity recognition results.

        .. note::

            This routine modify **doc** inplace.
        """
        return self._get('ner', doc)

    ########################################################################################################################

    def get_conparse(self, doc):
        """Apply constituency parsing.

        Arguments
        ---------
            doc : :class:`CkipDocument`
                The input document.

        Returns
        -------
            doc.conparse : :class:`~ckipnlp.container.parse.ParseParagraph`
                The constituency parsing sentences.

        .. note::

            This routine modify **doc** inplace.
        """
        return self._get('conparse', doc)
