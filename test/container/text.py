#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import json
import unittest

from .base import _TestCaseBase
from ckipnlp.container.text import *

################################################################################################################################

class TestTextParagraph(unittest.TestCase, _TestCaseBase):

    obj_class = TextParagraph

    text_in = [ '中文字喔', '啊哈哈哈', ]

    def _assertEqual(self, obj):
        self.assertEqual(len(obj), 2)

        self.assertEqual(obj[0], '中文字喔')
        self.assertEqual(obj[1], '啊哈哈哈')
