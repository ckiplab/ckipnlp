#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""The dummy CkipClassic Parser package"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

import numpy as np

################################################################################################################################

wspos2parser = {
    '中文字(Na)　耶(T)': ['#1:1.[0] S(Head:Nab:中文字|particle:Td:耶)#',],
    '啊(I)　哈(D)　哈哈(D)': ['#2:1.[0] %(particle:I:啊|manner:Dh:哈|manner:D:哈哈)',],
    '完蛋(VH)　了(T)': ['#3:1.[0] VP(Head:VH11:完蛋|particle:Ta:了)#',],
    '畢卡索(Nb)　他(Nh)　想(VE)': ['#4:1.[0] S(agent:NP(apposition:Nba:畢卡索|Head:Nhaa:他)|Head:VE2:想)#',],
    '但是(Cbb)　也(D)　沒有(VJ)　辦法(Na)': ['#5:1.[0] VP(contrast:Cbca:但是|evaluation:Dbb:也|Head:VJ3:沒有|range:NP(Head:Nac:辦法))#',],
}

################################################################################################################################

class CkipParser:

    def __init__(self, *args, **kwargs):
        pass

    def apply_list(self, wspos):
        for line in wspos:
            return self(line)

    def __call__(self, wspos):
        if wspos in wspos2parser:
            return wspos2parser[wspos]
        else:
            raise NotImplementedError(wspos)
