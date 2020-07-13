#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from test_core import *

def test():
    obj = CkipPipeline(sentence_parser=DriverFamily.CLASSIC)
    doc = CkipDocument(ws=SegParagraph.from_list(ws), pos=SegParagraph.from_list(pos))
    obj.get_parsed(doc)
    assert doc.parsed.to_list() == parsed
