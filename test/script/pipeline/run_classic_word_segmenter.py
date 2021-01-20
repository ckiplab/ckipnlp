#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

from _base import *

def test_classic_word_segmenter():
    obj = CkipPipeline(word_segmenter='classic')
    doc = CkipDocument(text=TextParagraph.from_list(text))
    obj.get_ws(doc)
    assert doc.ws.to_list() == [
        [ '中文字', '耶', '，', '啊哈', '哈哈', '。', ],
        [ '「', '完蛋', '了', '！', '」', '畢卡索', '他', '想', ],
    ]
