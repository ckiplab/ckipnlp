#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides container for word-segmented sentences.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from .base import (
    BaseList as _BaseList,
    BaseSentence0 as _BaseSentence0,
)

################################################################################################################################

class SegSentence(_BaseSentence0):
    """A word-segmented sentence."""

    item_class = str

    @classmethod
    def from_text(cls, data):
        """Construct an instance from text format.

        Parameters
        ----------
            data : str
                words segmented by ``'\\u3000'``.
        """
        return cls(map(cls._item_from_text, data.split('\u3000')))

    def to_text(self):
        """Transform to plain text.

        Return
        ------
            str
        """
        return '\u3000'.join(map(self._item_to_text, self))

class SegSentenceList(_BaseList):
    """A list of word-segmented sentences."""

    item_class = SegSentence
