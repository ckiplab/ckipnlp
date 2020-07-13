#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from base import _TestBase
from ckipnlp.container.parsed import *

################################################################################################################################

class TestParsedClause(_TestBase):

    obj_class = ParsedClause

    text_in = [ 'S(Head:Nab:中文字|particle:Td:耶)', '，', ]

    dict_in = {
        'clause': 'S(Head:Nab:中文字|particle:Td:耶)',
        'delim': '，',
    }

    def _assert_body(self, obj):
        assert len(obj) == 2
        assert obj.clause == self.text_in[0]
        assert obj.delim == self.text_in[1]

################################################################################################################################

class TestParsedSentence(_TestBase):

    obj_class = ParsedSentence

    text_in = [
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
        assert obj[0].clause == self.text_in[0][0]
        assert obj[0].delim == self.text_in[0][1]

        assert len(obj[1]) == 2
        assert obj[1].clause == self.text_in[1][0]
        assert obj[1].delim == self.text_in[1][1]

################################################################################################################################

class TestParsedParagraph(_TestBase):

    obj_class = ParsedParagraph

    text_in = [
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
        assert obj[0][0].clause == self.text_in[0][0][0]
        assert obj[0][0].delim == self.text_in[0][0][1]
        assert len(obj[0][1]) == 2
        assert obj[0][1].clause == self.text_in[0][1][0]
        assert obj[0][1].delim == self.text_in[0][1][1]

        assert len(obj[1]) == 3
        assert len(obj[1][0]) == 2
        assert obj[1][0].clause == self.text_in[1][0][0]
        assert obj[1][0].delim == self.text_in[1][0][1]
        assert len(obj[1][1]) == 2
        assert obj[1][1].clause == self.text_in[1][1][0]
        assert obj[1][1].delim == self.text_in[1][1][1]
        assert len(obj[1][2]) == 2
        assert obj[1][2].clause == self.text_in[1][2][0]
        assert obj[1][2].delim == self.text_in[1][2][1]
