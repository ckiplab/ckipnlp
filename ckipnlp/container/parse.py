#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides container for parsed sentences.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from .base import (
    BaseList as _BaseList,
)

################################################################################################################################

class ParseSentenceList(_BaseList):
    """A list of parsed sentence."""

    item_class = str

    @classmethod
    def _item_from_text(cls, data):
        return data

    @classmethod
    def _item_to_text(cls, item):
        return item

    @classmethod
    def _item_from_dict(cls, data):
        return data

    @classmethod
    def _item_to_dict(cls, item):
        return item
