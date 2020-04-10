#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from collections.abc import (
    Mapping as _Mapping,
)

from .core import (
    CkipPipeline as _CkipPipeline,
)

from ckipnlp.driver.base import (
    DriverType as _DriverType,
    DriverKind as _DriverKind,
    BaseDriver as _BaseDriver,
)

################################################################################################################################

class CkipCorefDocument(_Mapping):
    """The co-reference document.

    Attributes
    ----------
        ws
            :class:`SegParagraph` – The word-segmented sentences.
        pos
            :class:`SegParagraph` – The part-of-speech sentences.
        parsed
            :class:`ParsedParagraph` – The parsed-sentences.
    """

    __keys = ('ws', 'pos', 'parsed', 'coref',)

    def __init__(self, *, ws=None, pos=None, parsed=None, coref=None):
        self.ws = ws
        self.pos = pos
        self.parsed = parsed
        self.coref = coref

    def __len__(self):
        return len(self.__keys)

    def __iter__(self):
        yield from self.__keys

    def __getitem__(self, key):
        return getattr(self, key)

################################################################################################################################

class CkipCorefPipeline(_CkipPipeline):
    """The co-reference pipeline.

        Arguments
        ---------
        ner_chunker_kind : :class:`DriverKind`
            The type of named-entity recognition chunker. (`DriverKind.BUILTIN`)
    """

    def __init__(self, *, coref_chunker_kind=_DriverKind.BUILTIN, init=False, **kwargs,):
        super().__init__(init=init, **kwargs)

        # CoRef
        if coref_chunker_kind:
            assert self._wspos_driver.is_dummy, 'Co-reference pipeline is not compatible with CkipClassic word segmenter!'

        self._coref_chunker = _BaseDriver.get(_DriverType.COREF_CHUNKER, coref_chunker_kind)(init=init)

    def __call__(self, doc):
        corefdoc = CkipCorefDocument()
        self.get_coref(doc, corefdoc)
        return corefdoc

    def get_coref(self, doc, corefdoc):

        self.get_text(doc)
        self.get_ws(doc)
        self.get_pos(doc)
        self.get_ner(doc)

        # Update word segmentation
        if corefdoc.ws is None:
            corefdoc.ws = self._coref_chunker.transform_ws(doc.text, doc.ws, doc.ner)

        # Update POS-tagging
        if corefdoc.pos is None:
            corefdoc.pos = self.get_pos(corefdoc)
            self._coref_chunker.transform_pos(doc.text, corefdoc.pos, doc.ner)

        # Do parsing
        if corefdoc.parsed is None:
            corefdoc.parsed = self.get_parsed(corefdoc)

        # Get parser trees
        corefdoc.coref = self._coref_chunker(parsed=corefdoc.parsed)

        return corefdoc.coref
