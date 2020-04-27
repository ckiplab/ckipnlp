#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides containers for parsed sentences.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from .base import (
    BaseList0 as _BaseList0
)

################################################################################################################################

class ParsedParagraph(_BaseList0):
    """A list of parsed sentence.

    .. admonition:: Data Structure Examples

        Text/Dict/List format
            Used for :meth:`from_text`, :meth:`to_text`, :meth:`from_dict`, :meth:`to_dict`, :meth:`from_list`, and
            :meth:`to_list`.

            .. code-block:: python

                [
                    'S(Head:Nab:中文字|particle:Td:耶)',                     # Sentence 1
                    '%(particle:I:啊|manner:Dh:哈|manner:Dh:哈|time:Dh:哈)', # Sentence 2
                ]
    """

    item_class = str
