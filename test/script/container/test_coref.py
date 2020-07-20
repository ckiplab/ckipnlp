#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from base import _TestBase
from ckipnlp.container.coref import *

################################################################################################################################

class TestCorefToken(_TestBase):

    obj_class = CorefToken

    test_io_text = NotImplemented

    list_in = [ '畢卡索', (0, 'source'), (2, 2), ]
    dict_in = { 'word': '畢卡索', 'coref': (0, 'source'), 'idx': (2, 2), }

    def _assert_body(self, obj):
        assert obj.word == '畢卡索'
        assert obj.coref == (0, 'source')
        assert obj.idx == (2, 2)

    def test_to_text(self):
        obj = self.obj_class.from_list(self.list_in)
        text_out = obj.to_text()
        assert text_out == '畢卡索_0'

################################################################################################################################

class TestCorefSentence(_TestBase):

    obj_class = CorefSentence

    test_io_text = NotImplemented

    list_in = [
        [ '「', None, (0, None,), ],
        [ '完蛋', None, (1, 0,), ],
        [ '了', None, (1, 1,), ],
        [ '！」', None, (1, None,), ],
        [ '畢卡索', (0, 'source'), (2, 2,), ],
        [ '他', (0, 'target'), (2, 3,), ],
        [ '想', None, (2, 4,), ],
    ]

    dict_in = [
        { 'word': '「', 'coref': None, 'idx': (0, None,), },
        { 'word': '完蛋', 'coref': None, 'idx': (1, 0,), },
        { 'word': '了', 'coref': None, 'idx': (1, 1,), },
        { 'word': '！」', 'coref': None, 'idx': (1, None,), },
        { 'word': '畢卡索', 'coref': (0, 'source'), 'idx': (2, 2,), },
        { 'word': '他', 'coref': (0, 'target'), 'idx': (2, 3,), },
        { 'word': '想', 'coref': None, 'idx': (2, 4,), },
    ]

    def _assert_body(self, obj):
        assert len(obj) == 7

        assert obj[0].word == '「'
        assert obj[0].coref == None
        assert obj[0].idx == (0, None)

        assert obj[1].word == '完蛋'
        assert obj[1].coref == None
        assert obj[1].idx == (1, 0)

        assert obj[2].word == '了'
        assert obj[2].coref == None
        assert obj[2].idx == (1, 1)

        assert obj[3].word == '！」'
        assert obj[3].coref == None
        assert obj[3].idx == (1, None)

        assert obj[4].word == '畢卡索'
        assert obj[4].coref == (0, 'source')
        assert obj[4].idx == (2, 2)

        assert obj[5].word == '他'
        assert obj[5].coref == (0, 'target')
        assert obj[5].idx == (2, 3)

        assert obj[6].word == '想'
        assert obj[6].coref == None
        assert obj[6].idx == (2, 4)

################################################################################################################################

class TestCorefParagraph(_TestBase):

    obj_class = CorefParagraph

    test_io_text = NotImplemented

    list_in = [
        [
            [ '「', None, (0, None,), ],
            [ '完蛋', None, (1, 0,), ],
            [ '了', None, (1, 1,), ],
            [ '！」', None, (1, None,), ],
            [ '畢卡索', (0, 'source'), (2, 2,), ],
            [ '他', (0, 'target'), (2, 3,), ],
            [ '想', None, (2, 4,), ],
        ],
        [
            [ '但是', None, (0, 1,), ],
            [ None, (0, 'zero'), (0, None,), ],
            [ '也', None, (0, 2,), ],
            [ '沒有', None, (0, 3,), ],
            [ '辦法', None, (0, 5,), ],
        ],
    ]

    dict_in = [
        [
            { 'word': '「', 'coref': None, 'idx': (0, None,), },
            { 'word': '完蛋', 'coref': None, 'idx': (1, 0,), },
            { 'word': '了', 'coref': None, 'idx': (1, 1,), },
            { 'word': '！」', 'coref': None, 'idx': (1, None,), },
            { 'word': '畢卡索', 'coref': (0, 'source'), 'idx': (2, 2,), },
            { 'word': '他', 'coref': (0, 'target'), 'idx': (2, 3,), },
            { 'word': '想', 'coref': None, 'idx': (2, 4,), },
        ],
        [
            { 'word': '但是', 'coref': None, 'idx': (0, 1,), },
            { 'word': None, 'coref': (0, 'zero'), 'idx': (0, None,), },
            { 'word': '也', 'coref': None, 'idx': (0, 2,), },
            { 'word': '沒有', 'coref': None, 'idx': (0, 3,), },
            { 'word': '辦法', 'coref': None, 'idx': (0, 5,), },
        ],
    ]

    def _assert_body(self, obj):
        assert len(obj), 2

        assert len(obj[0]) == 7
        assert obj[0][0].word == '「'
        assert obj[0][0].coref == None
        assert obj[0][0].idx == (0, None)
        assert obj[0][1].word == '完蛋'
        assert obj[0][1].coref == None
        assert obj[0][1].idx == (1, 0)
        assert obj[0][2].word == '了'
        assert obj[0][2].coref == None
        assert obj[0][2].idx == (1, 1)
        assert obj[0][3].word == '！」'
        assert obj[0][3].coref == None
        assert obj[0][3].idx == (1, None)
        assert obj[0][4].word == '畢卡索'
        assert obj[0][4].coref == (0, 'source')
        assert obj[0][4].idx == (2, 2)
        assert obj[0][5].word == '他'
        assert obj[0][5].coref == (0, 'target')
        assert obj[0][5].idx == (2, 3)
        assert obj[0][6].word == '想'
        assert obj[0][6].coref == None
        assert obj[0][6].idx == (2, 4)

        assert len(obj[1]) == 5
        assert obj[1][0].word == '但是'
        assert obj[1][0].coref == None
        assert obj[1][0].idx == (0, 1)
        assert obj[1][1].word == None
        assert obj[1][1].coref == (0, 'zero')
        assert obj[1][1].idx == (0, None)
        assert obj[1][2].word == '也'
        assert obj[1][2].coref == None
        assert obj[1][2].idx == (0, 2)
        assert obj[1][3].word == '沒有'
        assert obj[1][3].coref == None
        assert obj[1][3].idx == (0, 3)
        assert obj[1][4].word == '辦法'
        assert obj[1][4].coref == None
        assert obj[1][4].idx == (0, 5)
