#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides containers for word-segmented sentences with part-of-speech-tags.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from typing import (
    NamedTuple as _NamedTuple,
)

from .base import (
    BaseTuple as _BaseTuple,
    BaseList as _BaseList,
    BaseSentence as _BaseSentence,
)

from .seg import (
    SegSentence as _SegSentence,
    SegSentenceList as _SegSentenceList,
)

################################################################################################################################

class _WsWord(_NamedTuple):
    word: str = None
    pos: str = None

class WsWord(_BaseTuple, _WsWord):
    """A word with POS-tag.

    Attributes
    ----------
        word
            *str* – the word.
        pos
            *str* – the POS-tag.

    Note
    ----
        This class is an subclass of :class:`tuple`. To change the attribute, please create a new instance instead.

    .. admonition:: Data Structure Examples

        Text format
            Used for :meth:`from_text` and :meth:`to_text`.

            .. code-block:: python

                '中文字(Na)'  # word / POS-tag

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                {
                    'word': '中文字', # word
                    'pos': 'Na',     # POS-tag
                }

        List format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                [
                    '中文字', # word
                    'Na',    # POS-tag
                ]
    """

    def __str__(self):
        return str(self.to_text())

    ########################################################################################################################

    @classmethod
    def from_text(cls, data):
        """Construct an instance from text format.

        Parameters
        ----------
            data : str
                text such as ``'中文字(Na)'``.

        .. note::
            - ``'中文字(Na)'`` -> word = ``'中文字'``, pos = ``'Na'``
            - ``'中文字'``     -> word = ``'中文字'``, pos = ``None``
        """
        return cls(*data.strip(')').rsplit('(', 1))

    def to_text(self):
        return '{}({})'.format(self.word, self.pos)

################################################################################################################################

class WsSentence(_BaseSentence):
    """A word-segmented sentence with POS-tags.

    .. admonition:: Data Structure Examples

        Text format
            Used for :meth:`from_text` and :meth:`to_text`.

            .. code-block:: python

                '中文字(Na)\\u3000喔(T)' # Words segmented by \\u3000 (full-width space)

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                [
                    { 'word': '中文字', 'pos': 'Na', }, # word 1
                    { 'word': '喔', 'pos': 'T', },     # word 2
                ]

        List format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                [
                    [ '中文字', 'Na', ],
                    [ '喔', 'T', ],
                ]
    """

    item_class = WsWord

    ########################################################################################################################

    @classmethod
    def from_word_pos(cls, word, pos):
        """Construct an instance a from a word sequence and a POS-tag sequence.

        Parameters
        ----------
            word : :class:`SegSentence`
                the word sentence.
            pos : :class:`SegSentence`
                the POS-tag sentence.
        """
        return cls(WsWord(w, p) for w, p in zip(word, pos))

    def to_word(self):
        """Transform to word sentence.

        Return
        ------
            :class:`SegSentence`
        """
        return _SegSentence.from_list((item.word for item in self))

    def to_pos(self):
        """Transform to POS-tag sentence.

        Return
        ------
            :class:`SegSentence`
        """
        return _SegSentence.from_list((item.pos for item in self))

################################################################################################################################

class WsSentenceList(_BaseList):
    """A list of word-segmented sentences with POS-tags.

    .. admonition:: Data Structure Examples

        Text format
            Used for :meth:`from_text` and :meth:`to_text`.

            .. code-block:: python

                [
                    '中文字(Na)\\u3000喔(T)', # Sentence 1
                    '啊哈(I)\\u3000哈哈(D)',  # Sentence 2
                ]

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                [
                    [ # Sentence 1
                        { 'word': '中文字', 'pos': 'Na', },
                        { 'word': '喔', 'pos': 'T', },
                    ],
                    [ # Sentence 2
                        { 'word': '啊哈', 'pos': 'I', },
                        { 'word': '哈哈', 'pos': 'D', },
                    ],
                ]

        List format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                [
                    [ # Sentence 1
                        [ '中文字', 'Na', ],
                        [ '喔', 'T', ],
                    ],
                    [ # Sentence 2
                        [ '啊哈', 'I', ],
                        [ '哈哈', 'D', ],
                    ],
                ]
    """

    item_class = WsSentence

    ########################################################################################################################

    @classmethod
    def from_word_pos(cls, word, pos):
        """Construct an instance a from word sequences and POS-tag sequences.

        Parameters
        ----------
            word : :class:`SegSentenceList`
                the word sentence list.
            pos : :class:`SegSentenceList`
                the POS-tag sentence list.
        """
        return cls((cls.item_class.from_word_pos(w, p) for w, p in zip(word, pos)))

    def to_word(self):
        """Transform to word sentence list.

        Return
        ------
            :class:`SegSentenceList`
        """
        return _SegSentenceList((item.to_word() for item in self))

    def to_pos(self):
        """Transform to POS-tag sentence list.

        Return
        ------
            :class:`SegSentenceList`
        """
        return _SegSentenceList((item.to_pos() for item in self))
