#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from test_core import *

def test():
    obj = CkipPipeline(word_segmenter=DriverFamily.CLASSIC, pos_tagger=DriverFamily.CLASSIC)
    doc = CkipDocument(text=TextParagraph.from_list(text))
    obj.get_pos(doc)
    assert doc.pos.to_list() == [
        [ 'Na', 'T', 'COMMACATEGORY', 'I', 'D', 'PERIODCATEGORY', ],
        [ 'PARENTHESISCATEGORY', 'VH', 'T', 'EXCLAMATIONCATEGORY', 'PARENTHESISCATEGORY', 'Nb', 'Nh', 'VE', ],
    ]
