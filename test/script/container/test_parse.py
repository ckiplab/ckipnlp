#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from _base import _TestBase
from ckipnlp.container.parse import *
from ckipnlp.container.util.parse_tree import ParseTree

################################################################################################################################

class TestParseClause(_TestBase):

    obj_class = ParseClause

    test_io_text = NotImplemented

    list_in = [ 'S(Head:Nab:中文字|particle:Td:耶)', '，', ]

    dict_in = {
        'clause': 'S(Head:Nab:中文字|particle:Td:耶)',
        'delim': '，',
    }

    def _assert_body(self, obj):
        assert len(obj) == 2
        assert obj.clause == self.list_in[0]
        assert obj.delim == self.list_in[1]

    def test_to_text(self):
        obj = self.obj_class.from_list(self.list_in)
        text_out = obj.to_text()
        assert text_out == self.list_in[0]

    def test_to_tree(self):
        obj = self.obj_class.from_list(self.list_in)
        tree_out = obj.to_tree()
        assert isinstance(tree_out, ParseTree)

    def test_to_tree_none(self):
        obj = self.obj_class()
        tree_out = obj.to_tree()
        assert tree_out is None

################################################################################################################################

class TestParseSentence(_TestBase):

    obj_class = ParseSentence

    test_io_text = NotImplemented

    list_in = [
        [ 'S(Head:Nab:中文字|particle:Td:耶)', '，', ],
        [ '%(particle:I:啊|manner:Dh:哈|manner:Dh:哈|time:Dh:哈)', '。', ],
    ]

    dict_in = [
        {
            'clause': 'S(Head:Nab:中文字|particle:Td:耶)',
            'delim': '，',
        },
        {
            'clause': '%(particle:I:啊|manner:Dh:哈|manner:Dh:哈|time:Dh:哈)',
            'delim': '。',
        },
    ]

    def _assert_body(self, obj):
        assert len(obj) == 2

        assert len(obj[0]) == 2
        assert obj[0].clause == self.list_in[0][0]
        assert obj[0].delim == self.list_in[0][1]

        assert len(obj[1]) == 2
        assert obj[1].clause == self.list_in[1][0]
        assert obj[1].delim == self.list_in[1][1]

################################################################################################################################

class TestParseParagraph(_TestBase):

    obj_class = ParseParagraph

    test_io_text = NotImplemented

    list_in = [
        [
            [ 'S(Head:Nab:中文字|particle:Td:耶)', '，', ],
            [ '%(particle:I:啊|manner:Dh:哈|manner:Dh:哈|time:Dh:哈)', '。', ],
        ],
        [
            [ None, '「', ],
            [ 'VP(Head:VH11:完蛋|particle:Ta:了)', '！」', ],
            [ 'S(agent:NP(apposition:Nba:畢卡索|Head:Nhaa:他)|Head:VE2:想)', '', ],
        ],
    ]

    dict_in = [
        [
            {
                'clause': 'S(Head:Nab:中文字|particle:Td:耶)',
                'delim': '，',
            },
            {
                'clause': '%(particle:I:啊|manner:Dh:哈|manner:Dh:哈|time:Dh:哈)',
                'delim': '。',
            },
        ],
        [
            {
                'clause': None,
                'delim': '「',
            },
            {
                'clause': 'VP(Head:VH11:完蛋|particle:Ta:了)',
                'delim': '！」',
            },
            {
                'clause': 'S(agent:NP(apposition:Nba:畢卡索|Head:Nhaa:他)|Head:VE2:想)',
                'delim': '',
            },
        ],
    ]

    def _assert_body(self, obj):
        assert len(obj) == 2

        assert len(obj[0]) == 2
        assert len(obj[0][0]) == 2
        assert obj[0][0].clause == self.list_in[0][0][0]
        assert obj[0][0].delim == self.list_in[0][0][1]
        assert len(obj[0][1]) == 2
        assert obj[0][1].clause == self.list_in[0][1][0]
        assert obj[0][1].delim == self.list_in[0][1][1]

        assert len(obj[1]) == 3
        assert len(obj[1][0]) == 2
        assert obj[1][0].clause == self.list_in[1][0][0]
        assert obj[1][0].delim == self.list_in[1][0][1]
        assert len(obj[1][1]) == 2
        assert obj[1][1].clause == self.list_in[1][1][0]
        assert obj[1][1].delim == self.list_in[1][1][1]
        assert len(obj[1][2]) == 2
        assert obj[1][2].clause == self.list_in[1][2][0]
        assert obj[1][2].delim == self.list_in[1][2][1]
