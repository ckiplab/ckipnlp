#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides containers for word-segmented sentences.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

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

                '中文字\u3000耶\u3000，\u3000啊\u3000哈\u3000哈哈\u3000。' # Words segmented by \\u3000 (full-width space)

        List/Dict format
            Used for :meth:`from_list`, :meth:`to_list`, :meth:`from_dict`, and :meth:`to_dict`.

            .. code-block:: python

                [ '中文字', '耶', '，', '啊', '哈', '哈哈', '。', ]

    .. note::

        This class is also used for part-of-speech tagging.

    """

    item_class = str

class SegParagraph(_BaseList):
    """A list of word-segmented sentences.

    .. admonition:: Data Structure Examples

        Text format
            Used for :meth:`from_text` and :meth:`to_text`.

            .. code-block:: python

                [
                    '中文字\u3000耶\u3000，\u3000啊\u3000哈\u3000哈\u3000。',        # Sentence 1
                    '「\u3000完蛋\u3000了\u3000！\u3000」\u3000，\u3000畢卡索\u3000他\u3000想', # Sentence 2
                ]

        List/Dict format
            Used for :meth:`from_list`, :meth:`to_list`, :meth:`from_dict`, and :meth:`to_dict`.

            .. code-block:: python

                [
                    [ '中文字', '耶', '，', '啊', '哈', '哈哈', '。', ],            # Sentence 1
                    [ '「', '完蛋', '了', '！', '」', '，', '畢卡索', '他', '想', ], # Sentence 2
                ]

    .. note::

        This class is also used for part-of-speech tagging.

    """

    item_class = SegSentence
