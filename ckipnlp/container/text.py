#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides container for text sentences.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from .base import (
    BaseList0 as _BaseList0
)

################################################################################################################################

class TextSentenceList(_BaseList0):
    """A list of text sentence."""

    item_class = str
