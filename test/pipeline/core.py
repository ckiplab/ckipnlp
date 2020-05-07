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

raw = '中文字喔，啊哈哈哈'
text = ['中文字喔', '啊哈哈哈']
ws = [
    [ '中文字', '喔', ],
    [ '啊', '哈', '哈', '哈', ],
]
pos = [
    [ 'Na', 'T', ],
    [ 'I', 'D', 'D', 'D', ],
]
ner = [
    [ [ '中文字', 'LANGUAGE', (0, 3), ], ],
    [],
]
parsed = [
    '#1:1.[0] S(Head:Nab:中文字|particle:Tc:喔)#',
    '#2:1.[0] %(particle:I:啊|manner:Dh:哈|manner:Dh:哈|time:Dh:哈)#',
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
#             [ '中文字', '喔', ],
#             [ '啊哈', '哈哈', ],
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
            [ 'Na', 'T', ],
            [ 'I', 'D', ],
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
