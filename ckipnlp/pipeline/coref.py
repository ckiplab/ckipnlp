#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides coreference resolution pipeline.
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

from .kernel import (
    CkipPipeline as _CkipPipeline,
)

################################################################################################################################

class CkipCorefDocument(_Mapping):
    """The coreference document.

    Attributes
    ----------
        ws : :class:`~ckipnlp.container.seg.SegParagraph`
            The word-segmented sentences.
        pos : :class:`~ckipnlp.container.seg.SegParagraph`
            The part-of-speech sentences.
        conparse : :class:`~ckipnlp.container.parse.ParseParagraph`
            The constituency sentences.
        coref : :class:`~ckipnlp.container.coref.CorefParagraph`
            The coreference resolution results.
    """

    __keys = ('ws', 'pos', 'conparse', 'coref',)

    def __init__(self, *, ws=None, pos=None, conparse=None, coref=None):
        self.ws = ws
        self.pos = pos
        self.conparse = conparse
        self.coref = coref

    def __len__(self):
        return len(self.__keys)

    def __iter__(self):
        yield from self.__keys

    def __getitem__(self, key):
        return getattr(self, key)

################################################################################################################################

class CkipCorefPipeline(_CkipPipeline):
    """The coreference resolution pipeline.

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

        coref_chunker : str
            The type of coreference resolution chunker.

    Other Parameters
    ----------------
        lazy : bool
            Lazy initialize the drivers.

        opts : Dict[str, Dict]
            The driver options. Key: driver name (e.g. `'sentence_segmenter'`); Value: a dictionary of options.
    """

    def __init__(self, *,
        coref_chunker='default',
        lazy=True,
        opts={},
        **kwargs,
    ):
        super().__init__(lazy=lazy, opts=opts, **kwargs)

        # CoRef
        if coref_chunker:
            assert self._wspos_driver.is_dummy, 'Coreference pipeline is not compatible with CkipClassic word segmenter!'

        self._coref_chunker = _DriverRegister.get('coref_chunker', coref_chunker)(
            lazy=lazy, **opts.get('coref_chunker', {}),
        )

    def __call__(self, doc):
        """Apply coreference delectation.

        Arguments
        ---------
            doc : :class:`~.kernel.CkipDocument`
                The input document.

        Returns
        -------
            corefdoc : :class:`CkipCorefDocument`
                The coreference document.

        .. note::

            **doc** is also modified if necessary dependencies (**ws**, **pos**, **ner**) is not computed yet.
        """

        corefdoc = CkipCorefDocument()
        self.get_coref(doc, corefdoc)
        return corefdoc

    def get_coref(self, doc, corefdoc):
        """Apply coreference delectation.

        Arguments
        ---------
            doc : :class:`~.kernel.CkipDocument`
                The input document.
            corefdoc : :class:`CkipCorefDocument`
                The input document for coreference.

        Returns
        -------
            corefdoc.coref : :class:`~ckipnlp.container.coref.CorefParagraph`
                The coreference results.

        .. note::

            This routine modify **corefdoc** inplace.

            **doc** is also modified if necessary dependencies (**ws**, **pos**, **ner**) is not computed yet.
        """
        self.get_text(doc)
        self.get_ws(doc)
        self.get_pos(doc)
        self.get_ner(doc)

        # Update word segmentation
        if corefdoc.ws is None:
            corefdoc.ws = self._coref_chunker.transform_ws(
                text=doc.text,
                ws=doc.ws,
                ner=doc.ner,
            )

        # Update POS-tagging
        if corefdoc.pos is None:
            corefdoc.pos = self.get_pos(corefdoc)
            self._coref_chunker.transform_pos(
                ws=corefdoc.ws,
                pos=corefdoc.pos,
                ner=doc.ner,
            )

        # Do parsing
        if corefdoc.conparse is None:
            corefdoc.conparse = self.get_conparse(corefdoc)

        # Do coreference resolution
        corefdoc.coref = self._coref_chunker(conparse=corefdoc.conparse)

        return corefdoc.coref
