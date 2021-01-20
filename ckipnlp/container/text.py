#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides containers for text sentences.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

from .base import (
    BaseList0 as _BaseList0
)

################################################################################################################################

class TextParagraph(_BaseList0):
    """A list of text sentence.

    .. admonition:: Data Structure Examples

        Text/List/Dict format
            Used for :meth:`from_text`, :meth:`to_text`, :meth:`from_list`, :meth:`to_list`, :meth:`from_dict`, and
            :meth:`to_dict`.

            .. code-block:: python

                [
                    '中文字耶，啊哈哈哈。',    # Sentence 1
                    '「完蛋了！」畢卡索他想', # Sentence 2
                ]
    """

    item_class = str
