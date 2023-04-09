#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2023 CKIP Lab'
__license__ = 'GPL-3.0'

from _base import *

################################################################################################################################

raw = '「完蛋了！」畢卡索他想\n但是也沒有辦法'
coref = [
    [
        [ '「', None, (0, None), ],
        [ '完蛋', None, (1, 1), ],
        [ '了', None, (1, 2), ],
        [ '！」', None, (1, None), ],
        [ '畢卡索', (0, 'source'), (2, 2), ],
        [ '他', (0, 'target'), (2, 3), ],
        [ '想', None, (2, 4), ],
    ],
    [
        [ '但是', None, (0, 1), ],
        [ None, (0, 'zero'), (0, None), ],
        [ '也', None, (0, 2), ],
        [ '沒有', None, (0, 3), ],
        [ '辦法', None, (0, 5), ],
    ],
]

################################################################################################################################

def test_coref_chunker():
    obj = CkipCorefPipeline()
    doc = CkipDocument(raw=raw)
    corefdoc = obj(doc)
    assert corefdoc.coref.to_list() == coref
