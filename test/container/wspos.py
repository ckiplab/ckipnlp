#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import json
import unittest

from .base import _TestCaseBase
from ckipnlp.container.wspos import *
from ckipnlp.container.seg import *

################################################################################################################################

class TestWsPosToken(unittest.TestCase, _TestCaseBase):

    obj_class = WsPosToken

    text_in = '中文字(Na)'
    dict_in = { 'word': '中文字', 'pos': 'Na', }
    list_in = [ '中文字', 'Na', ]

    def _assertEqual(self, obj):
        self.assertEqual(obj.word, '中文字')
        self.assertEqual(obj.pos, 'Na')

################################################################################################################################

class TestWsPosSentence(unittest.TestCase, _TestCaseBase):

    obj_class = WsPosSentence

    test_io_dict = NotImplemented
    test_io_list = NotImplemented
    test_io_json = NotImplemented

    text_in = '中文字(Na)　喔(T)'

    dict_in = {
        'word': [ '中文字', '喔', ],
        'pos': [ 'Na', 'T', ],
    }

    list_in = [
        [ '中文字', '喔', ],
        [ 'Na', 'T', ],
    ]

    def test_io_text(self):
        word_obj, pos_obj = self.obj_class.from_text(self.text_in)
        self._assertEqual(word_obj, pos_obj)
        text_out = self.obj_class.to_text(word_obj, pos_obj)
        self.assertEqual(text_out, self.text_in)

    def _assertEqual(self, word_obj, pos_obj):
        self.assertIsInstance(word_obj, SegSentence)
        self.assertEqual(len(word_obj), 2)
        self.assertEqual(word_obj[0], '中文字')
        self.assertEqual(word_obj[1], '喔')

        self.assertIsInstance(pos_obj, SegSentence)
        self.assertEqual(len(pos_obj), 2)
        self.assertEqual(pos_obj[0], 'Na')
        self.assertEqual(pos_obj[1], 'T')

################################################################################################################################

class TestWsPosParagraph(unittest.TestCase, _TestCaseBase):

    obj_class = WsPosParagraph

    test_io_dict = NotImplemented
    test_io_list = NotImplemented
    test_io_json = NotImplemented

    text_in = [ '中文字(Na)　喔(T)', '啊哈(I)　哈哈(D)', ]

    dict_in = {
        'word': [
            '中文字', '喔',
            '啊哈', '哈哈',
        ],
        'pos': [
            'Na', 'T',
            'I', 'D',
        ],
    }

    list_in = [
        [
            '中文字', '喔',
            '啊哈', '哈哈',
        ],
        [
            'Na', 'T',
            'I', 'D',
        ],
    ]

    def test_io_text(self):
        word_obj, pos_obj = self.obj_class.from_text(self.text_in)
        self._assertEqual(word_obj, pos_obj)
        text_out = self.obj_class.to_text(word_obj, pos_obj)
        self.assertEqual(text_out, self.text_in)

    def _assertEqual(self, word_obj, pos_obj):
        self.assertIsInstance(word_obj, SegParagraph)
        self.assertEqual(len(word_obj), 2)

        self.assertEqual(len(word_obj[0]), 2)
        self.assertEqual(word_obj[0][0], '中文字')
        self.assertEqual(word_obj[0][1], '喔')

        self.assertEqual(len(word_obj[1]), 2)
        self.assertEqual(word_obj[1][0], '啊哈')
        self.assertEqual(word_obj[1][1], '哈哈')


        self.assertIsInstance(pos_obj, SegParagraph)
        self.assertEqual(len(pos_obj), 2)

        self.assertEqual(len(pos_obj[0]), 2)
        self.assertEqual(pos_obj[0][0], 'Na')
        self.assertEqual(pos_obj[0][1], 'T')

        self.assertEqual(len(pos_obj[1]), 2)
        self.assertEqual(pos_obj[1][0], 'I')
        self.assertEqual(pos_obj[1][1], 'D')
