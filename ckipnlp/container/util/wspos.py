#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides containers for word-segmented sentences with part-of-speech-tags.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

from abc import (
    ABCMeta as _ABCMeta,
    abstractmethod as _abstractmethod,
)

from typing import (
    NamedTuple as _NamedTuple,
)

from ..base import (
    BaseTuple as _BaseTuple,
)

from ..seg import (
    SegSentence as _SegSentence,
    SegParagraph as _SegParagraph,
)

################################################################################################################################

def _token_from_text(data):
    """str -> Tuple[str, str]"""
    return data.strip().strip(')').rsplit('(', 1)

def _token_to_text(data):
    """Tuple[str, str] -> str"""
    return '{}({})'.format(*data)

def _sentence_from_text(data):
    """str -> Tuple[Iterable[str], Iterable[str]]"""
    return zip(*map(_token_from_text, data.split('\u3000')))

def _sentence_to_text(data):
    """Tuple[Iterable[str], Iterable[str]] -> str"""
    return '\u3000'.join(map(_token_to_text, zip(*data)))

def _paragraph_from_text(data):
    """Iterable[str] -> Tuple[Iterable[Iterable[str]], Iterable[Iterable[str]]]"""
    return zip(*map(_sentence_from_text, data))

def _paragraph_to_text(data):
    """Tuple[Iterable[Iterable[str]], Iterable[Iterable[str]]] -> Iterable[str]"""
    return map(_sentence_to_text, zip(*data))

################################################################################################################################

class _WsPosToken(_NamedTuple):
    word: str = None
    pos: str = None

class WsPosToken(_BaseTuple, _WsPosToken):
    """A word with POS-tag.

    Attributes
    ----------
        word : str
            the word.
        pos : str
            the POS-tag.

    Note
    ----
        This class is an subclass of *tuple*. To change the attribute, please create a new instance instead.

    .. admonition:: Data Structure Examples

        Text format
            Used for :meth:`from_text` and :meth:`to_text`.

            .. code-block:: python

                '中文字(Na)'  # word / POS-tag

        List format
            Used for :meth:`from_list` and :meth:`to_list`.

            .. code-block:: python

                [
                    '中文字', # word
                    'Na',    # POS-tag
                ]

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                {
                    'word': '中文字', # word
                    'pos': 'Na',     # POS-tag
                }
    """

    def __str__(self):
        return self.to_text()

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
        return cls(*_token_from_text(data))

    def to_text(self):
        return _token_to_text(self)

################################################################################################################################

class WsPosSentence(metaclass=_ABCMeta):
    """A helper class for data conversion of word-segmented and part-of-speech sentences."""

    @_abstractmethod
    def __init__(self):
        raise NotImplementedError  # pragma: no cover

    ########################################################################################################################

    @classmethod
    def from_text(cls, data):
        """Convert text format to word-segmented and part-of-speech sentences.

        Parameters
        ----------
            data : str
                text such as ``'中文字(Na)\\u3000耶(T)'``.

        Returns
        -------
            :class:`~ckipnlp.container.seg.SegSentence`
                the word sentence
            :class:`~ckipnlp.container.seg.SegSentence`
                the POS-tag sentence.
        """
        return tuple(map(_SegSentence.from_list, _sentence_from_text(data)))

    @staticmethod
    def to_text(word, pos):
        """Convert text format to word-segmented and part-of-speech sentences.

        Parameters
        ----------
            word : :class:`~ckipnlp.container.seg.SegSentence`
                the word sentence
            pos  : :class:`~ckipnlp.container.seg.SegSentence`
                the POS-tag sentence.

        Returns
        -------
            str
                text such as ``'中文字(Na)\\u3000耶(T)'``.
        """
        return _sentence_to_text((word, pos,))

################################################################################################################################

class WsPosParagraph(metaclass=_ABCMeta):
    """A helper class for data conversion of word-segmented and part-of-speech sentence lists."""

    @_abstractmethod
    def __init__(self):
        raise NotImplementedError  # pragma: no cover

    ########################################################################################################################

    @classmethod
    def from_text(cls, data):
        """Convert text format to word-segmented and part-of-speech sentence lists.

        Parameters
        ----------
            data : Sequence[str]
                list of sentences such as ``'中文字(Na)\\u3000耶(T)'``.

        Returns
        -------
            :class:`~.seg.SegParagraph`:
                the word sentence list
            :class:`~.seg.SegParagraph`:
                the POS-tag sentence list.
        """
        return tuple(map(_SegParagraph.from_list, _paragraph_from_text(data)))

    @staticmethod
    def to_text(word, pos):
        """Convert text format to word-segmented and part-of-speech sentence lists.

        Parameters
        ----------
            word : :class:`~.seg.SegParagraph`
                the word sentence list
            pos  : :class:`~.seg.SegParagraph`
                the POS-tag sentence list.

        Returns
        -------
            List[str]
                list of sentences such as ``'中文字(Na)\\u3000耶(T)'``.
        """
        return list(_paragraph_to_text((word, pos,)))
