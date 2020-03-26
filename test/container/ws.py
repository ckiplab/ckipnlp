#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import json
import unittest

from .base import _TestCaseBase
from ckipnlp.container.ws import *
from ckipnlp.container.seg import *

################################################################################################################################

class TestWsWord(unittest.TestCase, _TestCaseBase):

    obj_class = WsWord

    text_in = '中文字(Na)'
    dict_in = { 'word': '中文字', 'pos': 'Na', }

    list_in = [ '中文字', 'Na', ]

    def _assertEqual(self, obj):
        self.assertEqual(obj.word, '中文字')
        self.assertEqual(obj.pos, 'Na')

################################################################################################################################

class TestWsSentence(unittest.TestCase, _TestCaseBase):

    obj_class = WsSentence

    text_in = '中文字(Na)　喔(T)'

    dict_in = [
        { 'word': '中文字', 'pos': 'Na', },
        { 'word': '喔', 'pos': 'T', },
    ]

    list_in = [
        [ '中文字', 'Na', ],
        [ '喔', 'T', ],
    ]

    def _assertEqual(self, obj):
        self.assertEqual(len(obj), 2)
        self.assertEqual(obj[0].word, '中文字')
        self.assertEqual(obj[0].pos, 'Na')
        self.assertEqual(obj[1].word, '喔')
        self.assertEqual(obj[1].pos, 'T')

    def test_io_word_pos(self):
        word_in = SegSentence.from_list(['中文字', '喔'])
        pos_in = SegSentence.from_list(['Na', 'T'])

        obj = self.obj_class.from_word_pos(word_in, pos_in)
        self._assertEqual(obj)
        word_out = obj.to_word()
        pos_out = obj.to_pos()

        self.assertEqual(word_out, word_in)
        self.assertEqual(pos_out, pos_in)

################################################################################################################################

class TestWsSentenceList(unittest.TestCase, _TestCaseBase):

    obj_class = WsSentenceList

    text_in = [ '中文字(Na)　喔(T)', '啊哈(I)　哈哈(D)', ]

    dict_in = [
        [
            { 'word': '中文字', 'pos': 'Na', },
            { 'word': '喔', 'pos': 'T', },
        ],
        [
            { 'word': '啊哈', 'pos': 'I', },
            { 'word': '哈哈', 'pos': 'D', },
        ],
    ]

    list_in = [
        [
            [ '中文字', 'Na', ],
            [ '喔', 'T', ],
        ],
        [
            [ '啊哈', 'I', ],
            [ '哈哈', 'D', ],
        ],
    ]

    def _assertEqual(self, obj):
        self.assertEqual(len(obj), 2)

        self.assertEqual(len(obj[0]), 2)
        self.assertEqual(obj[0][0].word, '中文字')
        self.assertEqual(obj[0][0].pos, 'Na')
        self.assertEqual(obj[0][1].word, '喔')
        self.assertEqual(obj[0][1].pos, 'T')

        self.assertEqual(len(obj[1]), 2)
        self.assertEqual(obj[1][0].word, '啊哈')
        self.assertEqual(obj[1][0].pos, 'I')
        self.assertEqual(obj[1][1].word, '哈哈')
        self.assertEqual(obj[1][1].pos, 'D')

    def test_io_word_pos(self):
        word_in = SegSentenceList.from_list([['中文字', '喔'], ['啊哈', '哈哈']])
        pos_in = SegSentenceList.from_list([['Na', 'T'], ['I', 'D']])

        obj = self.obj_class.from_word_pos(word_in, pos_in)
        self._assertEqual(obj)
        word_out = obj.to_word()
        pos_out = obj.to_pos()

        self.assertEqual(word_out, word_in)
        self.assertEqual(pos_out, pos_in)
