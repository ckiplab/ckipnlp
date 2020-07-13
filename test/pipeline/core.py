#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import os
import unittest

from ckipnlp.pipeline import *
from ckipnlp.driver import DriverFamily
from ckipnlp.container import *

################################################################################################################################

import tensorflow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

################################################################################################################################

raw = '中文字耶，啊哈哈哈。\n「完蛋了！」畢卡索他想'
text = [
    '中文字耶，啊哈哈哈。',
    '「完蛋了！」畢卡索他想',
]
ws = [
    [ '中文字', '耶', '，', '啊', '哈', '哈哈', '。', ],
    [ '「', '完蛋', '了', '！', '」', '畢卡索', '他', '想', ],
]
pos = [
    [ 'Na', 'T', 'COMMACATEGORY', 'I', 'D', 'D', 'PERIODCATEGORY', ],
    [ 'PARENTHESISCATEGORY', 'VH', 'T', 'EXCLAMATIONCATEGORY', 'PARENTHESISCATEGORY', 'Nb', 'Nh', 'VE', ],
]
ner = [
    [ [ '中文字', 'LANGUAGE', (0, 3), ], ],
    [ [ '畢卡索', 'PERSON', (6, 9), ], ],
]
parsed = [
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

################################################################################################################################

class TestSentenceSegmenter(unittest.TestCase):

    def test(self):
        obj = CkipPipeline(sentence_segmenter=DriverFamily.BUILTIN)
        doc = CkipDocument(raw=raw)
        obj.get_text(doc)
        self.assertSequenceEqual(doc.text.to_list(), text)

################################################################################################################################

class TestTaggerWordSegmenter(unittest.TestCase):

    def test(self):
        obj = CkipPipeline(word_segmenter=DriverFamily.TAGGER)
        doc = CkipDocument(text=TextParagraph.from_list(text))
        obj.get_ws(doc)
        self.assertSequenceEqual(doc.ws.to_list(), ws)

################################################################################################################################

# class TestClassicWordSegmenter(unittest.TestCase):

#     def test(self):
#         obj = CkipPipeline(word_segmenter=DriverFamily.CLASSIC)
#         doc = CkipDocument(text=TextParagraph.from_list(text))
#         obj.get_ws(doc)
#         self.assertSequenceEqual(doc.ws.to_list(), [
#             [ '中文字', '耶', '，', '啊哈', '哈哈', '。', ],
#             [ '「', '完蛋', '了', '！', '」', '畢卡索', '他', '想', ],
#         ])

################################################################################################################################

class TestTaggerPosTagger(unittest.TestCase):

    def test(self):
        obj = CkipPipeline(pos_tagger=DriverFamily.TAGGER)
        doc = CkipDocument(ws=SegParagraph.from_list(ws))
        obj.get_pos(doc)
        self.assertSequenceEqual(doc.pos.to_list(), pos)

################################################################################################################################

class TestClassicWordSegmenterPosTagger(unittest.TestCase):

    def test(self):
        obj = CkipPipeline(word_segmenter=DriverFamily.CLASSIC, pos_tagger=DriverFamily.CLASSIC)
        doc = CkipDocument(text=TextParagraph.from_list(text))
        obj.get_pos(doc)
        self.assertSequenceEqual(doc.pos.to_list(), [
            [ 'Na', 'T', 'COMMACATEGORY', 'I', 'D', 'PERIODCATEGORY', ],
            [ 'PARENTHESISCATEGORY', 'VH', 'T', 'EXCLAMATIONCATEGORY', 'PARENTHESISCATEGORY', 'Nb', 'Nh', 'VE', ],
        ])

################################################################################################################################

class TestTaggerNerChunker(unittest.TestCase):

    def test(self):
        obj = CkipPipeline(ner_chunker=DriverFamily.TAGGER)
        doc = CkipDocument(ws=SegParagraph.from_list(ws), pos=SegParagraph.from_list(pos))
        obj.get_ner(doc)
        self.assertSequenceEqual(doc.ner.to_list(), ner)

################################################################################################################################

# class TestClassicSentenceParser(unittest.TestCase):

#     def test(self):
#         obj = CkipPipeline(sentence_parser=DriverFamily.CLASSIC)
#         doc = CkipDocument(ws=SegParagraph.from_list(ws), pos=SegParagraph.from_list(pos))
#         obj.get_parsed(doc)
#         self.assertSequenceEqual(doc.parsed.to_list(), parsed)
