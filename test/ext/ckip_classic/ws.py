#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""The dummy CkipClassic WS package"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

import numpy as np

################################################################################################################################

base_text = [
    '中文字耶，啊哈哈哈。',
    '「完蛋了！」畢卡索他想',
]
base_wspos = [
    '中文字(Na)　耶(T)　，(COMMACATEGORY)　啊哈(I)　哈哈(D)　。(PERIODCATEGORY)',
    '「(PARENTHESISCATEGORY)　完蛋(VH)　了(T)　！(EXCLAMATIONCATEGORY)　」(PARENTHESISCATEGORY)　畢卡索(Nb)　他(Nh)　想(VE)',
]

################################################################################################################################

class CkipWs:

    def __init__(self, *args, **kwargs):
        pass

    def apply_list(self, text):
        if np.array_equal(text, base_text):
            return base_wspos
        else:
            raise NotImplementedError(text)
