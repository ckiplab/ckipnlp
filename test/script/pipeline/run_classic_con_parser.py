#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2023 CKIP Lab'
__license__ = 'GPL-3.0'

from _base import *

def test_classic_con_parser():
    obj = CkipPipeline(con_parser='classic')
    doc = CkipDocument(ws=SegParagraph.from_list(ws), pos=SegParagraph.from_list(pos))
    obj.get_conparse(doc)
    assert doc.conparse.to_list() == [
        [
            [ 'S(Head:Nab:中文字|particle:Td:耶)', '，', ],
            [ '%(particle:I:啊|manner:Dh:哈|manner:D:哈哈)', '。', ],
        ],
        [
            [ None, '「', ],
            [ 'VP(Head:VH11:完蛋|particle:Ta:了)', '！」', ],
            [ 'S(agent:NP(apposition:Nba:畢卡索|Head:Nhaa:他)|Head:VE2:想)', '', ],
        ],
    ]
