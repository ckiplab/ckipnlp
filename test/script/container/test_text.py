#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from _base import _TestBase
from ckipnlp.container.text import *

################################################################################################################################

class TestTextParagraph(_TestBase):

    obj_class = TextParagraph

    text_in = [
        '中文字耶，啊哈哈哈。',
        '「完蛋了！」畢卡索他想',
    ]

    def _assert_body(self, obj):
        assert len(obj) == 2

        assert obj[0] == '中文字耶，啊哈哈哈。'
        assert obj[1] == '「完蛋了！」畢卡索他想'
