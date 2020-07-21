#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from base import *

################################################################################################################################

def test_sentence_segmenter():
    obj = CkipPipeline(sentence_segmenter='default')
    doc = CkipDocument(raw=raw)
    obj.get_text(doc)
    assert doc.text.to_list() == text

################################################################################################################################

def test_tagger_word_segmenter():
    obj = CkipPipeline(word_segmenter='tagger')
    doc = CkipDocument(text=TextParagraph.from_list(text))
    obj.get_ws(doc)
    assert doc.ws.to_list() == ws

################################################################################################################################

def test_tagger_pos_tagger():
    obj = CkipPipeline(pos_tagger='tagger')
    doc = CkipDocument(ws=SegParagraph.from_list(ws))
    obj.get_pos(doc)
    assert doc.pos.to_list() == pos

################################################################################################################################

def test_tagger_ner_chunker():
    obj = CkipPipeline(ner_chunker='tagger')
    doc = CkipDocument(ws=SegParagraph.from_list(ws), pos=SegParagraph.from_list(pos))
    obj.get_ner(doc)
    assert doc.ner.to_list() == ner
