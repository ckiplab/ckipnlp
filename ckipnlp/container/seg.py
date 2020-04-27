#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides containers for word-segmented sentences.
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
    """A word-segmented sentence.

    .. admonition:: Data Structure Examples

        Text format
            Used for :meth:`from_text` and :meth:`to_text`.

            .. code-block:: python

                '中文字\u3000喔' # Words segmented by \\u3000 (full-width space)

        Dict/List format
            Used for :meth:`from_dict`, :meth:`to_dict`, :meth:`from_list`, and :meth:`to_list`.

            .. code-block:: python

                [ '中文字', '喔', ]

    .. note::

        This class is also used for part-of-speech tagging.

    """

    item_class = str

    @classmethod
    def from_text(cls, data):
        return cls(map(cls._item_from_text, data.split('\u3000')))

    def to_text(self):
        return '\u3000'.join(map(self._item_to_text, self))

class SegParagraph(_BaseList):
    """A list of word-segmented sentences.

    .. admonition:: Data Structure Examples

        Text format
            Used for :meth:`from_text` and :meth:`to_text`.

            .. code-block:: python

                [
                    '中文字\u3000喔',     # Sentence 1
                    '啊\u3000哈\u3000哈\u3000哈', # Sentence 2
                ]

        Dict/List format
            Used for :meth:`from_dict`, :meth:`to_dict`,  :meth:`from_list`, and :meth:`to_list`.

            .. code-block:: python

                [
                    [ '中文字', '喔', ],         # Sentence 1
                    [ '啊', '哈', '哈', '哈', ], # Sentence 2
                ]

    .. note::

        This class is also used for part-of-speech tagging.

    """

    item_class = SegSentence
