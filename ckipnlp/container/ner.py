#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides container for NER sentences.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from enum import (
    IntEnum as _IntEnum,
    auto as _enum_auto,
)

from typing import (
    NamedTuple as _NamedTuple,
    Tuple as _Tuple,
)

from .base import (
    Base as _Base,
    BaseList as _BaseList,
    BaseSentence as _BaseSentence,
)

################################################################################################################################

class NerType(_IntEnum):
    CARDINAL = _enum_auto()
    DATE = _enum_auto()
    EVENT = _enum_auto()
    FAC = _enum_auto()
    GPE = _enum_auto()
    LANGUAGE = _enum_auto()
    LAW = _enum_auto()
    LOC = _enum_auto()
    MONEY = _enum_auto()
    NORP = _enum_auto()
    ORDINAL = _enum_auto()
    ORG = _enum_auto()
    PERCENT = _enum_auto()
    PERSON = _enum_auto()
    PRODUCT = _enum_auto()
    QUANTITY = _enum_auto()
    TIME = _enum_auto()
    WORK_OF_ART = _enum_auto()

################################################################################################################################

class _NerToken(_NamedTuple):
    word: str
    ner: NerType
    idx: _Tuple[int, int]

class NerToken(_Base, _NerToken):
    """A NER token.

    Attributes
    ----------
        word : str
            the token word.
        ner : str
            the NER-tag.
        idx : Tuple[int, int]
            the staring / ending index.
    """

    to_text = NotImplemented
    from_text = NotImplemented

    @classmethod
    def from_dict(cls, data):
        """Construct an instance from python built-in containers.

        Parameters
        ----------
            data : dict
                dictionary such as ``{ 'word': '中文字', 'ner': 'LANGUAGE', idx: (0, 3) }``
        """
        return cls(**data)

    def to_dict(self):
        """Transform to python built-in containers.

        Return
        ------
            dict
        """
        return self._asdict() # pylint: disable=no-member

################################################################################################################################

class NerSentence(_BaseSentence):
    """A list of NER sentence."""

    item_class = NerToken

    to_text = NotImplemented
    from_text = NotImplemented


class NerSentenceList(_BaseList):
    """A list of NER sentence."""

    item_class = NerSentence

    to_text = NotImplemented
    from_text = NotImplemented
