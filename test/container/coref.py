#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import json
import unittest

from .base import _TestCaseBase
from ckipnlp.container.coref import *

################################################################################################################################

class TestCorefToken(unittest.TestCase, _TestCaseBase):

    obj_class = CorefToken

    test_io_text = NotImplemented

    list_in = [ '畢卡索', (0, 'source'), 2, ]
    dict_in = { 'word': '畢卡索', 'coref': (0, 'source'), 'idx': 2, }

    def _assertEqual(self, obj):
        self.assertEqual(obj.word, '畢卡索')
        self.assertSequenceEqual(obj.coref, (0, 'source'))
        self.assertEqual(obj.idx, 2)

################################################################################################################################

class TestCorefSentence(unittest.TestCase, _TestCaseBase):

    obj_class = CorefSentence

    test_io_text = NotImplemented

    list_in = [
        [ '畢卡索', (0, 'source'), 2, ],
        [ '他', (0, 'target'), 3, ],
        [ '想', None, 4, ],
    ]

    dict_in = [
        { 'word': '畢卡索', 'coref': (0, 'source'), 'idx': 2, },
        { 'word': '他', 'coref': (0, 'target'), 'idx': 3, },
        { 'word': '想', 'coref': None, 'idx': 4, },
    ]

    def _assertEqual(self, obj):
        self.assertEqual(len(obj), 3)

        self.assertEqual(obj[0].word, '畢卡索')
        self.assertSequenceEqual(obj[0].coref, (0, 'source'))
        self.assertEqual(obj[0].idx, 2)

        self.assertEqual(obj[1].word, '他')
        self.assertSequenceEqual(obj[1].coref, (0, 'target'))
        self.assertEqual(obj[1].idx, 3)

        self.assertEqual(obj[2].word, '想')
        self.assertEqual(obj[2].coref, None)
        self.assertEqual(obj[2].idx, 4)

################################################################################################################################

class TestCorefParagraph(unittest.TestCase, _TestCaseBase):

    obj_class = CorefParagraph

    test_io_text = NotImplemented

    list_in = [
        [
            [ '畢卡索', (0, 'source'), 2, ],
            [ '他', (0, 'target'), 3, ],
            [ '想', None, 4, ],
        ],
        [
            [ None, (0, 'zero'), None, ],
            [ '完蛋', None, 1, ],
            [ '了', None, 2, ],
        ],
    ]

    dict_in = [
        [
            { 'word': '畢卡索', 'coref': (0, 'source'), 'idx': 2, },
            { 'word': '他', 'coref': (0, 'target'), 'idx': 3, },
            { 'word': '想', 'coref': None, 'idx': 4, },
        ],
        [
            { 'word': None, 'coref': (0, 'zero'), 'idx': None, },
            { 'word': '完蛋', 'coref': None, 'idx': 1, },
            { 'word': '了', 'coref': None, 'idx': 2, },
        ],
    ]

    def _assertEqual(self, obj):
        self.assertEqual(len(obj), 2)

        self.assertEqual(len(obj[0]), 3)
        self.assertEqual(obj[0][0].word, '畢卡索')
        self.assertSequenceEqual(obj[0][0].coref, (0, 'source'))
        self.assertEqual(obj[0][0].idx, 2)
        self.assertEqual(obj[0][1].word, '他')
        self.assertSequenceEqual(obj[0][1].coref, (0, 'target'))
        self.assertEqual(obj[0][1].idx, 3)
        self.assertEqual(obj[0][2].word, '想')
        self.assertEqual(obj[0][2].coref, None)
        self.assertEqual(obj[0][2].idx, 4)

        self.assertEqual(len(obj[1]), 3)
        self.assertEqual(obj[1][0].word, None)
        self.assertSequenceEqual(obj[1][0].coref, (0, 'zero'))
        self.assertEqual(obj[1][0].idx, None)
        self.assertEqual(obj[1][1].word, '完蛋')
        self.assertEqual(obj[1][1].coref, None)
        self.assertEqual(obj[1][1].idx, 1)
        self.assertEqual(obj[1][2].word, '了')
        self.assertEqual(obj[1][2].coref, None)
        self.assertEqual(obj[1][2].idx, 2)
