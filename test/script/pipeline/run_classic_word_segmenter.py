#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from base import *

def test_classic_word_segmenter():
    obj = CkipPipeline(word_segmenter=DriverFamily.CLASSIC)
    doc = CkipDocument(text=TextParagraph.from_list(text))
    obj.get_ws(doc)
    assert doc.ws.to_list() == [
        [ '中文字', '耶', '，', '啊哈', '哈哈', '。', ],
        [ '「', '完蛋', '了', '！', '」', '畢卡索', '他', '想', ],
    ]
