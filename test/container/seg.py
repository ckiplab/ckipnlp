#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import json
import unittest

from .base import _TestCaseBase
from ckipnlp.container.seg import *

################################################################################################################################

class TestSegSentence(unittest.TestCase, _TestCaseBase):

    obj_class = SegSentence

    text_in = '中文字\u3000喔'
    dict_in = [ '中文字', '喔', ]

    def _assertEqual(self, obj):
        self.assertEqual(len(obj), 2)
        self.assertEqual(obj[0], '中文字')
        self.assertEqual(obj[1], '喔')

################################################################################################################################

class TestSegSentenceList(unittest.TestCase, _TestCaseBase):

    obj_class = SegSentenceList

    text_in = [ '中文字\u3000喔', '啊哈\u3000哈哈', ]

    dict_in = [
        [ '中文字', '喔', ],
        [ '啊哈', '哈哈', ],
    ]

    def _assertEqual(self, obj):
        self.assertEqual(len(obj), 2)

        self.assertEqual(len(obj[0]), 2)
        self.assertEqual(obj[0][0], '中文字')
        self.assertEqual(obj[0][1], '喔')

        self.assertEqual(len(obj[1]), 2)
        self.assertEqual(obj[1][0], '啊哈')
        self.assertEqual(obj[1][1], '哈哈')
