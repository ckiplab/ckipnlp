#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import json
import unittest

from .base import _TestCaseBase
from ckipnlp.container.ner import *

################################################################################################################################

class TestNerToken(unittest.TestCase, _TestCaseBase):

    obj_class = NerToken

    dict_in = { 'word': '中文字', 'ner': 'LANGUAGE', 'idx': (0, 3) }
    list_in = [ '中文字', 'LANGUAGE', (0, 3) ]

    test_io_text = NotImplemented

    def _assertEqual(self, obj):
        self.assertEqual(obj.word, '中文字')
        self.assertEqual(obj.ner, 'LANGUAGE')
        self.assertSequenceEqual(obj.idx, (0, 3))

    def test_io_tagger(self):
        tagger_in = (0, 3, 'LANGUAGE', '中文字',)

        obj = self.obj_class.from_tagger(tagger_in)
        self._assertEqual(obj)
        tagger_out = obj.to_tagger()

        self.assertEqual(tagger_out, tagger_in)

################################################################################################################################

class TestNerSentence(unittest.TestCase, _TestCaseBase):

    obj_class = NerSentence

    dict_in = [
        { 'word': '美國', 'ner': 'GPE', 'idx': (0, 2) },
        { 'word': '參議院', 'ner': 'ORG', 'idx': (3, 5) },
    ]

    list_in = [
        [ '美國', 'GPE', (0, 2) ],
        [ '參議院', 'ORG', (3, 5) ],
    ]

    test_io_text = NotImplemented

    def _assertEqual(self, obj):
        self.assertEqual(len(obj), 2)

        self.assertEqual(obj[0].word, '美國')
        self.assertEqual(obj[0].ner, 'GPE')
        self.assertSequenceEqual(obj[0].idx, (0, 2))

        self.assertEqual(obj[1].word, '參議院')
        self.assertEqual(obj[1].ner, 'ORG')
        self.assertSequenceEqual(obj[1].idx, (3, 5))

    def test_io_tagger(self):
        tagger_in = [
            (0, 2, 'GPE', '美國',),
            (3, 5, 'ORG', '參議院',),
        ]

        obj = self.obj_class.from_tagger(tagger_in)
        self._assertEqual(obj)
        tagger_out = obj.to_tagger()

        self.assertEqual(tagger_out, tagger_in)

################################################################################################################################

class TestNerSentenceList(unittest.TestCase, _TestCaseBase):

    obj_class = NerSentenceList

    dict_in = [
        [
            { 'word': '中文字', 'ner': 'LANGUAGE', 'idx': (0, 3) },
        ],
        [
            { 'word': '美國', 'ner': 'GPE', 'idx': (0, 2) },
            { 'word': '參議院', 'ner': 'ORG', 'idx': (3, 5) },
        ],
    ]

    list_in = [
        [
            [ '中文字', 'LANGUAGE', (0, 3) ],
        ],
        [
            [ '美國', 'GPE', (0, 2) ],
            [ '參議院', 'ORG', (3, 5) ],
        ],
    ]

    test_io_text = NotImplemented

    def test_io_tagger(self):
        tagger_in = [
            [
                (0, 3, 'LANGUAGE', '中文字',),
            ],
            [
                (0, 2, 'GPE', '美國',),
                (3, 5, 'ORG', '參議院',),
            ],
        ]

        obj = self.obj_class.from_tagger(tagger_in)
        self._assertEqual(obj)
        tagger_out = obj.to_tagger()

        self.assertEqual(tagger_out, tagger_in)

    def _assertEqual(self, obj):
        self.assertEqual(len(obj), 2)

        self.assertEqual(len(obj[0]), 1)
        self.assertEqual(obj[0][0].word, '中文字')
        self.assertEqual(obj[0][0].ner, 'LANGUAGE')
        self.assertSequenceEqual(obj[0][0].idx, (0, 3))

        self.assertEqual(len(obj[1]), 2)
        self.assertEqual(obj[1][0].word, '美國')
        self.assertEqual(obj[1][0].ner, 'GPE')
        self.assertSequenceEqual(obj[1][0].idx, (0, 2))
        self.assertEqual(obj[1][1].word, '參議院')
        self.assertEqual(obj[1][1].ner, 'ORG')
        self.assertSequenceEqual(obj[1][1].idx, (3, 5))
