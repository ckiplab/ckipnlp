#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

from _base import _TestBase
from ckipnlp.container.ner import *

################################################################################################################################

class TestNerToken(_TestBase):

    obj_class = NerToken

    test_io_text = NotImplemented

    list_in = [ '中文字', 'LANGUAGE', (0, 3), ]
    dict_in = { 'word': '中文字', 'ner': 'LANGUAGE', 'idx': (0, 3), }
    tagger_in = ( 0, 3, 'LANGUAGE', '中文字', )

    def _assert_body(self, obj):
        assert obj.word == '中文字'
        assert obj.ner == 'LANGUAGE'
        assert obj.idx, (0, 3)

    def test_io_tagger(self):

        obj = self.obj_class.from_tagger(self.tagger_in)
        self._assert_body(obj)
        tagger_out = obj.to_tagger()

        assert tagger_out == self.tagger_in

################################################################################################################################

class TestNerSentence(_TestBase):

    obj_class = NerSentence

    test_io_text = NotImplemented

    list_in = [
        [ '美國', 'GPE', (0, 2), ],
        [ '參議院', 'ORG', (3, 5), ],
    ]

    dict_in = [
        { 'word': '美國', 'ner': 'GPE', 'idx': (0, 2), },
        { 'word': '參議院', 'ner': 'ORG', 'idx': (3, 5), },
    ]

    tagger_in = [
        ( 0, 2, 'GPE', '美國', ),
        ( 3, 5, 'ORG', '參議院', ),
    ]

    def _assert_body(self, obj):
        assert len(obj) == 2

        assert obj[0].word == '美國'
        assert obj[0].ner == 'GPE'
        assert obj[0].idx, (0, 2)

        assert obj[1].word == '參議院'
        assert obj[1].ner == 'ORG'
        assert obj[1].idx, (3, 5)

    def test_io_tagger(self):

        obj = self.obj_class.from_tagger(self.tagger_in)
        self._assert_body(obj)
        tagger_out = obj.to_tagger()

        assert tagger_out == self.tagger_in

################################################################################################################################

class TestNerParagraph(_TestBase):

    obj_class = NerParagraph

    test_io_text = NotImplemented

    list_in = [
        [
            [ '中文字', 'LANGUAGE', (0, 3), ],
        ],
        [
            [ '美國', 'GPE', (0, 2), ],
            [ '參議院', 'ORG', (3, 5), ],
        ],
    ]

    dict_in = [
        [
            { 'word': '中文字', 'ner': 'LANGUAGE', 'idx': (0, 3), },
        ],
        [
            { 'word': '美國', 'ner': 'GPE', 'idx': (0, 2), },
            { 'word': '參議院', 'ner': 'ORG', 'idx': (3, 5), },
        ],
    ]

    tagger_in = [
        [
            ( 0, 3, 'LANGUAGE', '中文字', ),
        ],
        [
            ( 0, 2, 'GPE', '美國', ),
            ( 3, 5, 'ORG', '參議院', ),
        ],
    ]

    def test_io_tagger(self):
        obj = self.obj_class.from_tagger(self.tagger_in)
        self._assert_body(obj)
        tagger_out = obj.to_tagger()

        assert tagger_out == self.tagger_in

    def _assert_body(self, obj):
        assert len(obj) == 2

        assert len(obj[0]) == 1
        assert obj[0][0].word == '中文字'
        assert obj[0][0].ner == 'LANGUAGE'
        assert obj[0][0].idx, (0, 3)

        assert len(obj[1]) == 2
        assert obj[1][0].word == '美國'
        assert obj[1][0].ner == 'GPE'
        assert obj[1][0].idx, (0, 2)
        assert obj[1][1].word == '參議院'
        assert obj[1][1].ner == 'ORG'
        assert obj[1][1].idx, (3, 5)
