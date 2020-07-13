#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from base import _TestBase
from ckipnlp.container.util.wspos import *
from ckipnlp.container.seg import *

################################################################################################################################

class TestWsPosToken(_TestBase):

    obj_class = WsPosToken

    text_in = '中文字(Na)'
    list_in = [ '中文字', 'Na', ]
    dict_in = { 'word': '中文字', 'pos': 'Na', }

    def _assert_body(self, obj):
        assert obj.word == '中文字'
        assert obj.pos == 'Na'

################################################################################################################################

class TestWsPosSentence(_TestBase):

    obj_class = WsPosSentence

    test_io_list = NotImplemented
    test_io_dict = NotImplemented
    test_io_json = NotImplemented

    text_in = '中文字(Na)　耶(T)'

    list_in = [
        [ '中文字', '耶', ],
        [ 'Na', 'T', ],
    ]

    dict_in = {
        'word': [ '中文字', '耶', ],
        'pos': [ 'Na', 'T', ],
    }

    def test_io_text(self):
        word_obj, pos_obj = self.obj_class.from_text(self.text_in)
        self._assert_body(word_obj, pos_obj)
        text_out = self.obj_class.to_text(word_obj, pos_obj)
        assert text_out, self.text_in

    def _assert_body(self, word_obj, pos_obj):
        assert isinstance(word_obj, SegSentence)
        assert len(word_obj) == 2
        assert word_obj[0] == '中文字'
        assert word_obj[1] == '耶'

        assert isinstance(pos_obj, SegSentence)
        assert len(pos_obj) == 2
        assert pos_obj[0] == 'Na'
        assert pos_obj[1] == 'T'

################################################################################################################################

class TestWsPosParagraph(_TestBase):

    obj_class = WsPosParagraph

    test_io_list = NotImplemented
    test_io_dict = NotImplemented
    test_io_json = NotImplemented

    text_in = [ '中文字(Na)　耶(T)', '啊(I)　哈(D)　哈(D)　哈(D)', ]

    list_in = [
        [
            '中文字', '耶',
            '啊', '哈', '哈', '哈',
        ],
        [
            'Na', 'T',
            'I', 'D', 'D', 'D',
        ],
    ]

    dict_in = {
        'word': [
            '中文字', '耶',
            '啊', '哈', '哈', '哈',
        ],
        'pos': [
            'Na', 'T',
            'I', 'D', 'D', 'D',
        ],
    }

    def test_io_text(self):
        word_obj, pos_obj = self.obj_class.from_text(self.text_in)
        self._assert_body(word_obj, pos_obj)
        text_out = self.obj_class.to_text(word_obj, pos_obj)
        assert text_out, self.text_in

    def _assert_body(self, word_obj, pos_obj):
        assert isinstance(word_obj, SegParagraph)
        assert len(word_obj) == 2

        assert len(word_obj[0]) == 2
        assert word_obj[0][0] == '中文字'
        assert word_obj[0][1] == '耶'

        assert len(word_obj[1]) == 4
        assert word_obj[1][0] == '啊'
        assert word_obj[1][1] == '哈'
        assert word_obj[1][2] == '哈'
        assert word_obj[1][3] == '哈'


        assert isinstance(pos_obj, SegParagraph)
        assert len(pos_obj) == 2

        assert len(pos_obj[0]) == 2
        assert pos_obj[0][0] == 'Na'
        assert pos_obj[0][1] == 'T'

        assert len(pos_obj[1]) == 4
        assert pos_obj[1][0] == 'I'
        assert pos_obj[1][1] == 'D'
        assert pos_obj[1][2] == 'D'
        assert pos_obj[1][3] == 'D'
