#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from base import _TestBase
from ckipnlp.container.util.parsed_tree import *

################################################################################################################################

class TestParsedNodeData(_TestBase):

    obj_class = ParsedNodeData

    test_io_list = NotImplemented

    text_in = 'Head:Na:中文字'
    dict_in = { 'role': 'Head', 'pos': 'Na', 'word': '中文字', }

    def _assert_body(self, obj):
        assert obj.role == 'Head'
        assert obj.pos == 'Na'
        assert obj.word == '中文字'

    def test_no_word(self):
        obj = self.obj_class.from_text('Head:Na')
        assert obj.role == 'Head'
        assert obj.pos == 'Na'
        assert obj.word == None

    def test_no_role(self):
        obj = self.obj_class.from_text('Na')
        assert obj.role == None
        assert obj.pos == 'Na'
        assert obj.word == None

################################################################################################################################

class TestParsedTree(_TestBase):
    """
    我的早餐、午餐和晚餐都在比賽中被吃掉了

    S[0]
    ├── goal:NP[1]
    │   ├── possessor:N‧的[2]
    │   │   ├── head:Nhaa:我[3]
    │   │   └── Head:DE:的[4]
    │   └── Head:Nab[5]
    │       ├── DUMMY1:Nab[6]
    │       │   ├── DUMMY1:Nab:早餐[7]
    │       │   ├── Head:Caa:、[8]
    │       │   └── DUMMY2:Naa:午餐[9]
    │       ├── Head:Caa:和[10]
    │       └── DUMMY2:Nab:晚餐[11]
    ├── quantity:Dab:都[12]
    ├── condition:PP[13]
    │   ├── Head:P21:在[14]
    │   └── DUMMY:GP[15]
    │       ├── DUMMY:NP[16]
    │       │   └── Head:Nac:比賽[17]
    │       └── Head:Ng:中[18]
    ├── agent:PP[19]
    │   └── Head:P02:被[20]
    ├── Head:VC31:吃掉[21]
    └── aspect:Di:了[22]
    """

    obj_class = ParsedTree

    test_io_list = NotImplemented

    text_in = 'S(goal:NP(possessor:N‧的(head:Nhaa:我|Head:DE:的)|Head:Nab(DUMMY1:Nab(DUMMY1:Nab:早餐|Head:Caa:、|DUMMY2:Naa:午餐)|Head:Caa:和|DUMMY2:Nab:晚餐))|quantity:Dab:都|condition:PP(Head:P21:在|DUMMY:GP(DUMMY:NP(Head:Nac:比賽)|Head:Ng:中))|agent:PP(Head:P02:被)|Head:VC31:吃掉|aspect:Di:了)'

    dict_in = {
        'id': 0,
        'data': { 'role': None, 'pos': 'S', 'word': None, },
        'children': [
            {
                'id': 1,
                'data': { 'role': 'goal', 'pos': 'NP', 'word': None, },
                'children': [
                    {
                        'id': 2,
                        'data': { 'role': 'possessor', 'pos': 'N‧的', 'word': None, },
                        'children': [
                            {
                                'id': 3,
                                'data': { 'role': 'head', 'pos': 'Nhaa', 'word': '我', },
                                'children': [],
                            },
                            {
                                'id': 4,
                                'data': { 'role': 'Head', 'pos': 'DE', 'word': '的', },
                                'children': [],
                            },
                        ],
                    },
                    {
                        'id': 5,
                        'data': { 'role': 'Head', 'pos': 'Nab', 'word': None, },
                        'children': [
                            {
                                'id': 6,
                                'data': { 'role': 'DUMMY1', 'pos': 'Nab', 'word': None, },
                                'children': [
                                    {
                                        'id': 7,
                                        'data': { 'role': 'DUMMY1', 'pos': 'Nab', 'word': '早餐', },
                                        'children': [],
                                    },
                                    {
                                        'id': 8,
                                        'data': { 'role': 'Head', 'pos': 'Caa', 'word': '、', },
                                        'children': [],
                                    },
                                    {
                                        'id': 9,
                                        'data': { 'role': 'DUMMY2', 'pos': 'Naa', 'word': '午餐', },
                                        'children': [],
                                    },
                                ],
                            },
                            {
                                'id': 10,
                                'data': { 'role': 'Head', 'pos': 'Caa', 'word': '和', },
                                'children': [],
                            },
                            {
                                'id': 11,
                                'data': { 'role': 'DUMMY2', 'pos': 'Nab', 'word': '晚餐', },
                                'children': [],
                            },
                        ],
                    },
                ],
            },
            {
                'id': 12,
                'data': { 'role': 'quantity', 'pos': 'Dab', 'word': '都', },
                'children': [],
            },
            {
                'id': 13,
                'data': { 'role': 'condition', 'pos': 'PP', 'word': None, },
                'children': [
                    {
                        'id': 14,
                        'data': { 'role': 'Head', 'pos': 'P21', 'word': '在', },
                        'children': [],
                    },
                    {
                        'id': 15,
                        'data': { 'role': 'DUMMY', 'pos': 'GP', 'word': None, },
                        'children': [
                            {
                                'id': 16,
                                'data': { 'role': 'DUMMY', 'pos': 'NP', 'word': None, },
                                'children': [
                                    {
                                        'id': 17,
                                        'data': { 'role': 'Head', 'pos': 'Nac', 'word': '比賽', },
                                        'children': [],
                                    },
                                ],
                            },
                            {
                                'id': 18,
                                'data': { 'role': 'Head', 'pos': 'Ng', 'word': '中', },
                                'children': [],
                            },
                        ],
                    },
                ],
            },
            {
                'id': 19,
                'data': { 'role': 'agent', 'pos': 'PP', 'word': None, },
                'children': [
                    {
                        'id': 20,
                        'data': { 'role': 'Head', 'pos': 'P02', 'word': '被', },
                        'children': [],
                    },
                ],
            },
            {
                'id': 21,
                'data': { 'role': 'Head', 'pos': 'VC31', 'word': '吃掉', },
                'children': [],
            },
            {
                'id': 22,
                'data': { 'role': 'aspect', 'pos': 'Di', 'word': '了', },
                'children': [],
            },
        ],
    }

    penn_in = [
        'S',
        [
            'goal:NP',
            [
                'possessor:N‧的',
                [ 'head:Nhaa', '我', ],
                [ 'Head:DE', '的', ],
            ],
            [
                'Head:Nab',
                [
                    'DUMMY1:Nab',
                    [ 'DUMMY1:Nab', '早餐', ],
                    [ 'Head:Caa', '、', ],
                    [ 'DUMMY2:Naa', '午餐', ],
                ],
                [ 'Head:Caa', '和' ],
                [ 'DUMMY2:Nab', '晚餐' ],
            ],
        ],
        [ 'quantity:Dab', '都', ],
        [
            'condition:PP',
            [ 'Head:P21', '在', ],
            [
                'DUMMY:GP',
                [
                    'DUMMY:NP',
                    [ 'Head:Nac', '比賽' ],
                ],
                [ 'Head:Ng', '中', ],
            ],
        ],
        [
            'agent:PP',
            [ 'Head:P02', '被', ],
        ],
        [ 'Head:VC31', '吃掉', ],
        [ 'aspect:Di', '了', ],
    ]

    def _assert_body(self, obj):
        assert len(obj), 23
        self._assert_body_node(obj, 0, None, None, 'S', None)
        self._assert_body_node(obj, 1, 0, 'goal', 'NP', None)
        self._assert_body_node(obj, 2, 1, 'possessor', 'N‧的', None)
        self._assert_body_node(obj, 3, 2, 'head', 'Nhaa', '我')
        self._assert_body_node(obj, 4, 2, 'Head', 'DE', '的')
        self._assert_body_node(obj, 5, 1, 'Head', 'Nab', None)
        self._assert_body_node(obj, 6, 5, 'DUMMY1', 'Nab', None)
        self._assert_body_node(obj, 7, 6, 'DUMMY1', 'Nab', '早餐')
        self._assert_body_node(obj, 8, 6, 'Head', 'Caa', '、')
        self._assert_body_node(obj, 9, 6, 'DUMMY2', 'Naa', '午餐')
        self._assert_body_node(obj, 10, 5, 'Head', 'Caa', '和')
        self._assert_body_node(obj, 11, 5, 'DUMMY2', 'Nab', '晚餐')
        self._assert_body_node(obj, 12, 0, 'quantity', 'Dab', '都')
        self._assert_body_node(obj, 13, 0, 'condition', 'PP', None)
        self._assert_body_node(obj, 14, 13, 'Head', 'P21', '在')
        self._assert_body_node(obj, 15, 13, 'DUMMY', 'GP', None)
        self._assert_body_node(obj, 16, 15, 'DUMMY', 'NP', None)
        self._assert_body_node(obj, 17, 16, 'Head', 'Nac', '比賽')
        self._assert_body_node(obj, 18, 15, 'Head', 'Ng', '中')
        self._assert_body_node(obj, 19, 0, 'agent', 'PP', None)
        self._assert_body_node(obj, 20, 19, 'Head', 'P02', '被')
        self._assert_body_node(obj, 21, 0, 'Head', 'VC31', '吃掉')
        self._assert_body_node(obj, 22, 0, 'aspect', 'Di', '了')

    def _assert_body_node(self, obj, node_id, parent_id, role, pos, word):
        node = obj[node_id]
        node_data = node.data
        if parent_id is not None:
            assert obj.parent(node_id).identifier == parent_id
        else:
            assert obj.parent(node_id) == None
        assert node.tag == node_data.to_text()
        assert node_data.role == role
        assert node_data.pos == pos
        assert node_data.word == word

    def test_io_penn(self):

        obj = self.obj_class.from_penn(self.penn_in)
        self._assert_body(obj)
        penn_out = obj.to_penn()

        assert penn_out == self.penn_in

    def test_get_heads_semantic(self):
        obj = self.obj_class.from_text(self.text_in)
        self._assert_get_heads(obj, 0, [21], semantic=True)
        self._assert_get_heads(obj, 1, [7, 9, 11], semantic=True)
        self._assert_get_heads(obj, 2, [3], semantic=True)
        self._assert_get_heads(obj, 5, [7, 9, 11], semantic=True)
        self._assert_get_heads(obj, 6, [7, 9], semantic=True)
        self._assert_get_heads(obj, 13, [17], semantic=True)
        self._assert_get_heads(obj, 15, [17], semantic=True)
        self._assert_get_heads(obj, 16, [17], semantic=True)
        self._assert_get_heads(obj, 19, [20], semantic=True)

    def test_get_heads_syntactic(self):
        obj = self.obj_class.from_text(self.text_in)
        self._assert_get_heads(obj, 0, [21], semantic=False)
        self._assert_get_heads(obj, 1, [10], semantic=False)
        self._assert_get_heads(obj, 2, [4], semantic=False)
        self._assert_get_heads(obj, 5, [10], semantic=False)
        self._assert_get_heads(obj, 6, [8], semantic=False)
        self._assert_get_heads(obj, 13, [14], semantic=False)
        self._assert_get_heads(obj, 15, [18], semantic=False)
        self._assert_get_heads(obj, 16, [17], semantic=False)
        self._assert_get_heads(obj, 19, [20], semantic=False)

    def _assert_get_heads(self, obj, node_id, heads_id, *, semantic):
        heads_id_out = [node.identifier for node in obj.get_heads(node_id, semantic=semantic)]
        assert heads_id_out == heads_id

    def test_get_relations_semantic(self):
        obj = self.obj_class.from_text(self.text_in)
        rels_id = {
            (7, 3, 'possessor',),
            (9, 3, 'possessor',),
            (11, 3, 'possessor',),
            (21, 7, 'goal',),
            (21, 9, 'goal',),
            (21, 11, 'goal',),
            (21, 12, 'quantity',),
            (21, 17, 'condition',),
            (21, 20, 'agent',),
            (21, 22, 'aspect',),
        }
        rels_id_out = {
            (rel.head.identifier, rel.tail.identifier, rel.relation.data.role)
                for rel in obj.get_relations(semantic=True)
        }
        assert rels_id_out == rels_id

    def test_get_relations_syntactic(self):
        obj = self.obj_class.from_text(self.text_in)
        rels_id = {
            (4, 3, 'head',),
            (8, 7, 'DUMMY1',),
            (8, 9, 'DUMMY2',),
            (10, 4, 'possessor',),
            (10, 8, 'DUMMY1',),
            (10, 11, 'DUMMY2',),
            (14, 18, 'DUMMY',),
            (18, 17, 'DUMMY',),
            (21, 10, 'goal',),
            (21, 12, 'quantity',),
            (21, 14, 'condition',),
            (21, 20, 'agent',),
            (21, 22, 'aspect',),
        }
        rels_id_out = {
            (rel.head.identifier, rel.tail.identifier, rel.relation.data.role)
                for rel in obj.get_relations(semantic=False)
        }
        assert rels_id_out == rels_id
