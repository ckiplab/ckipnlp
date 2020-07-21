#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""The dummy CkipTagger package"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import numpy as np

################################################################################################################################

base_text = [
    '中文字耶，啊哈哈哈。',
    '「完蛋了！」畢卡索他想',
]
base_ws = [
    [ '中文字', '耶', '，', '啊', '哈', '哈哈', '。', ],
    [ '「', '完蛋', '了', '！', '」', '畢卡索', '他', '想', ],
]
base_pos = [
    [ 'Na', 'T', 'COMMACATEGORY', 'I', 'D', 'D', 'PERIODCATEGORY', ],
    [ 'PARENTHESISCATEGORY', 'VH', 'T', 'EXCLAMATIONCATEGORY', 'PARENTHESISCATEGORY', 'Nb', 'Nh', 'VE', ],
]
base_ner = [
    [ (0, 3, 'LANGUAGE', '中文字',), ],
    [ (6, 9, 'PERSON', '畢卡索',), ],
]

################################################################################################################################

coref_text = [
    '「完蛋了！」畢卡索他想',
    '但是也沒有辦法',
]
coref_ws = [
    [ '「', '完蛋', '了', '！', '」', '畢卡索', '他', '想', ],
    [ '但是', '也', '沒有', '辦法', ],
]
coref_pos = [
    [ 'PARENTHESISCATEGORY', 'VH', 'T', 'EXCLAMATIONCATEGORY', 'PARENTHESISCATEGORY', 'Nb', 'Nh', 'VE', ],
    [ 'Cbb', 'D', 'VJ', 'Na', ],
]
coref_ner = [
    [ (6, 9, 'PERSON', '畢卡索',), ],
    [],
]

################################################################################################################################

def construct_dictionary(*args, **kwargs):
    return {}

################################################################################################################################

class WS:

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, text):
        if np.array_equal(text, base_text):
            return base_ws
        elif np.array_equal(text, coref_text):
            return coref_ws
        else:
            raise NotImplementedError(text)

################################################################################################################################

class POS:

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, ws):
        if np.array_equal(ws, base_ws):
            return base_pos
        elif np.array_equal(ws, coref_ws):
            return coref_pos
        else:
            raise NotImplementedError(ws)

################################################################################################################################

class NER:

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, ws, pos):
        if np.array_equal(ws, base_ws) and np.array_equal(pos, base_pos):
            return base_ner
        elif np.array_equal(ws, coref_ws) and np.array_equal(pos, coref_pos):
            return coref_ner
        else:
            raise NotImplementedError((ws, pos,))
