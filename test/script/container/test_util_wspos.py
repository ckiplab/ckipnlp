#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

import pytest

from _base import _TestBase
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

    def test_str(self):
        obj = self.obj_class.from_text(self.text_in)
        assert str(obj) == self.text_in

################################################################################################################################

class TestWsPosSentence(_TestBase):

    obj_class = WsPosSentence

    test_io_list = NotImplemented
    test_io_dict = NotImplemented
    test_io_json = NotImplemented

    text_in = '中文字(Na)　耶(T)　，(COMMACATEGORY)　啊(I)　哈(D)　哈哈(D)　。(PERIODCATEGORY)'

    def test_io_text(self):
        word_obj, pos_obj = self.obj_class.from_text(self.text_in)
        self._assert_body(word_obj, pos_obj)
        text_out = self.obj_class.to_text(word_obj, pos_obj)
        assert text_out, self.text_in

    def test_init(self):
        with pytest.raises(TypeError):
            obj = self.obj_class()

    def _assert_body(self, word_obj, pos_obj):
        assert isinstance(word_obj, SegSentence)
        assert len(word_obj) == 7
        assert word_obj == [ '中文字', '耶', '，', '啊', '哈', '哈哈', '。', ]

        assert isinstance(pos_obj, SegSentence)
        assert len(pos_obj) == 7
        assert pos_obj == [ 'Na', 'T', 'COMMACATEGORY', 'I', 'D', 'D', 'PERIODCATEGORY', ]

################################################################################################################################

class TestWsPosParagraph(_TestBase):

    obj_class = WsPosParagraph

    test_io_list = NotImplemented
    test_io_dict = NotImplemented
    test_io_json = NotImplemented

    text_in = [
        '中文字(Na)　耶(T)　，(COMMACATEGORY)　啊(I)　哈(D)　哈哈(D)　。(PERIODCATEGORY)',
        '「(PARENTHESISCATEGORY)　完蛋(VH)　了(T)　！(EXCLAMATIONCATEGORY)　」(PARENTHESISCATEGORY)　，(COMMACATEGORY)　畢卡索(Nb)　他(Nh)　想(VE)',
    ]

    def test_io_text(self):
        word_obj, pos_obj = self.obj_class.from_text(self.text_in)
        self._assert_body(word_obj, pos_obj)
        text_out = self.obj_class.to_text(word_obj, pos_obj)
        assert text_out, self.text_in

    def test_init(self):
        with pytest.raises(TypeError):
            obj = self.obj_class()

    def _assert_body(self, word_obj, pos_obj):
        assert isinstance(word_obj, SegParagraph)
        assert len(word_obj) == 2

        assert len(word_obj[0]) == 7
        assert word_obj[0] == [ '中文字', '耶', '，', '啊', '哈', '哈哈', '。', ]

        assert len(word_obj[1]) == 9
        assert word_obj[1] == [ '「', '完蛋', '了', '！', '」', '，', '畢卡索', '他', '想', ]


        assert isinstance(pos_obj, SegParagraph)
        assert len(pos_obj) == 2

        assert len(pos_obj[0]) == 7
        assert pos_obj[0] == [ 'Na', 'T', 'COMMACATEGORY', 'I', 'D', 'D', 'PERIODCATEGORY', ]

        assert len(pos_obj[1]) == 9
        assert pos_obj[1] == [ 'PARENTHESISCATEGORY', 'VH', 'T', 'EXCLAMATIONCATEGORY', 'PARENTHESISCATEGORY', 'COMMACATEGORY', 'Nb', 'Nh', 'VE', ]
