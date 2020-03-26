#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides container for NER sentences.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from typing import (
    NamedTuple as _NamedTuple,
    Tuple as _Tuple,
)

from .base import (
    BaseTuple as _BaseTuple,
    BaseList as _BaseList,
    BaseSentence as _BaseSentence,
)

################################################################################################################################

class _NerToken(_NamedTuple):
    word: str
    ner: str
    idx: _Tuple[int, int]

class NerToken(_BaseTuple, _NerToken):
    """A NER token.

    Attributes
    ----------
        word : str
            the token word.
        ner : str
            the NER-tag.
        idx : Tuple[int, int]
            the starting / ending index.
    """

    to_text = NotImplemented
    from_text = NotImplemented

    ########################################################################################################################

    @classmethod
    def from_tagger(cls, data):
        """Construct an instance a from CkipTagger format.

        Parameters
        ----------
            data : Tuple[int, int, str, str]
                starting index, ending index, NER-tag, token word.
        """
        idx0, idx1, ner, word = data
        return cls(word=word, ner=ner, idx=(idx0, idx1,))  # pylint: disable=no-value-for-parameter

    def to_tagger(self):
        """Transform to CkipTagger format.

        Return
        ------
            Tuple[int, int, str, str]
        """
        return (*self.idx, self.ner, self.word)

################################################################################################################################

class NerSentence(_BaseSentence):
    """A list of NER sentence."""

    item_class = NerToken

    to_text = NotImplemented
    from_text = NotImplemented

    ########################################################################################################################

    @classmethod
    def from_tagger(cls, data):
        """Construct an instance a from CkipTagger format.

        Parameters
        ----------
            data : Sequence[Tuple[int, int, str, str]]
                starting index, ending index, NER-tag, token word.
        """
        return cls(map(cls.item_class.from_tagger, data))

    def to_tagger(self):
        """Transform to CkipTagger format.

        Return
        ------
            List[Tuple[int, int, str, str]]
        """
        return list(item.to_tagger() for item in self)

################################################################################################################################

class NerSentenceList(_BaseList):
    """A list of NER sentence."""

    item_class = NerSentence

    to_text = NotImplemented
    from_text = NotImplemented

    ########################################################################################################################

    @classmethod
    def from_tagger(cls, data):
        """Construct an instance a from CkipTagger format.

        Parameters
        ----------
            data : Sequence[Sequence[Tuple[int, int, str, str]]]
                starting index, ending index, NER-tag, token word.
        """
        return cls(map(cls.item_class.from_tagger, data))

    def to_tagger(self):
        """Transform to CkipTagger format.

        Return
        ------
            List[List[Tuple[int, int, str, str]]]
        """
        return list(item.to_tagger() for item in self)
