#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides container for word-segmented sentences with part-of-speech-tags.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from typing import (
    NamedTuple as _NamedTuple,
)

from .base import (
    Base as _Base,
    BaseList as _BaseList,
    BaseSentence as _BaseSentence,
)

################################################################################################################################

class _WsWord(_NamedTuple):
    word: str = None
    pos: str = None

class WsWord(_Base, _WsWord):
    """A word with POS-tag.

    Attributes
    ----------
        word : str
            the word.
        pos : str
            the POS-tag.
    """

    @classmethod
    def from_text(cls, data):
        """Construct an instance from text format.

        Parameters
        ----------
            data : str
                text such as ``'中文字(Na)'``.

        Note
        ----
            - ``'中文字(Na)'`` -> word = ``'中文字'``, pos = ``'Na'``
            - ``'中文字'``     -> word = ``'中文字'``, pos = ``None``
        """
        return cls(*data.strip(')').rsplit('(', 1))

    def to_text(self):
        """Transform to plain text.

        Return
        ------
            str
        """
        return '{}({})'.format(self.word, self.pos)

    @classmethod
    def from_dict(cls, data):
        """Construct an instance from python built-in containers.

        Parameters
        ----------
            data : dict
                dictionary such as ``{ 'word': '中文字', 'pos': 'Na' }``
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

class WsSentence(_BaseSentence):
    """A word-segmented sentence with POS-tags."""

    item_class = WsWord

class WsSentenceList(_BaseList):
    """A list of word-segmented sentences with POS-tags."""

    item_class = WsSentence
