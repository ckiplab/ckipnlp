#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

from _base import _TestBase
from ckipnlp.container.seg import *

################################################################################################################################

class TestSegSentence(_TestBase):

    obj_class = SegSentence

    text_in = '中文字\u3000耶\u3000，\u3000啊\u3000哈\u3000哈哈\u3000。'
    list_in = [ '中文字', '耶', '，', '啊', '哈', '哈哈', '。', ]

    def _assert_body(self, obj):
        assert len(obj) == 7
        assert obj == self.list_in

################################################################################################################################

class TestSegParagraph(_TestBase):

    obj_class = SegParagraph

    text_in = [
        '中文字\u3000耶\u3000，\u3000啊\u3000哈\u3000哈哈\u3000。',
        '「\u3000完蛋\u3000了\u3000！\u3000」\u3000，\u3000畢卡索\u3000他\u3000想',
    ]

    list_in = [
        [ '中文字', '耶', '，', '啊', '哈', '哈哈', '。', ],
        [ '「', '完蛋', '了', '！', '」', '，', '畢卡索', '他', '想', ],
    ]

    def _assert_body(self, obj):
        assert len(obj) == 2

        assert len(obj[0]) == 7
        assert obj[0] == self.list_in[0]

        assert len(obj[1]) == 9
        assert obj[1] == self.list_in[1]
