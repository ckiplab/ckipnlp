#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import json
import unittest

from ckipnlp.util.parser import *

################################################################################################################################

class _TestCaseBase:

    @property
    def obj_class(self):
        raise NotImplementedError

    @property
    def text_in(self):
        raise NotImplementedError

    @property
    def dict_in(self):
        raise NotImplementedError

    @property
    def json_in(self):
        return json.dumps(self.dict_in, ensure_ascii=False)

    def _assertEqual(self, obj):
        raise NotImplementedError

    def test_from_to_text(self):
        obj = self.obj_class.from_text(self.text_in)
        self._assertEqual(obj)
        text_out = obj.to_text()
        self.assertEqual(text_out, self.text_in)

    def test_from_to_dict(self):
        obj = self.obj_class.from_dict(self.dict_in)
        self._assertEqual(obj)
        dict_out = obj.to_dict()
        self.assertEqual(dict_out, self.dict_in)

    def test_from_to_json(self):
        obj = self.obj_class.from_json(self.json_in)
        self._assertEqual(obj)
        json_out = obj.to_json(ensure_ascii=False)
        self.assertEqual(json_out, self.json_in)

################################################################################################################################

class TestParserNodeData(unittest.TestCase, _TestCaseBase):

    obj_class = ParserNodeData

    text_in = 'Head:Na:中文字'
    dict_in = { 'role': 'Head', 'pos': 'Na', 'term': '中文字' }

    def _assertEqual(self, obj):
        self.assertEqual(obj.role, 'Head')
        self.assertEqual(obj.pos, 'Na')
        self.assertEqual(obj.term, '中文字')

    def test_no_term(self):
        obj = self.obj_class.from_text('Head:Na')
        self.assertEqual(obj.role, 'Head')
        self.assertEqual(obj.pos, 'Na')
        self.assertEqual(obj.term, None)

    def test_no_role(self):
        obj = self.obj_class.from_text('Na')
        self.assertEqual(obj.role, None)
        self.assertEqual(obj.pos, 'Na')
        self.assertEqual(obj.term, None)

################################################################################################################################

class TestParserTree(unittest.TestCase, _TestCaseBase):

    obj_class = ParserTree

    text_in = 'S(theme:NP(possessor:N‧的(head:Nhaa:我|Head:DE:的)|Head:Nab(DUMMY1:Nab(DUMMY1:Nab:早餐|Head:Caa:、|DUMMY2:Naa:午餐)|Head:Caa:和|DUMMY2:Nab:晚餐))|quantity:Dab:都|target:PP(Head:P30:往|DUMMY:NP(property:Ncb:天|Head:Ncda:上))|Head:VA11:飛|aspect:Di:了)'

    dict_in = {
        'id': 0,
        'data': { 'role': None, 'pos': 'S', 'term': None, },
        'children': [
            {
                'id': 1,
                'data': { 'role': 'theme', 'pos': 'NP', 'term': None, },
                'children': [
                    {
                        'id': 2,
                        'data': { 'role': 'possessor', 'pos': 'N‧的', 'term': None, },
                        'children': [
                            {
                                'id': 3,
                                'data': { 'role': 'head', 'pos': 'Nhaa', 'term': '我', },
                                'children': [],
                            },
                            {
                                'id': 4,
                                'data': { 'role': 'Head', 'pos': 'DE', 'term': '的', },
                                'children': [],
                            },
                        ],
                    },
                    {
                        'id': 5,
                        'data': { 'role': 'Head', 'pos': 'Nab', 'term': None, },
                        'children': [
                            {
                                'id': 6,
                                'data': { 'role': 'DUMMY1', 'pos': 'Nab', 'term': None, },
                                'children': [
                                    {
                                        'id': 7,
                                        'data': { 'role': 'DUMMY1', 'pos': 'Nab', 'term': '早餐', },
                                        'children': [],
                                    },
                                    {
                                        'id': 8,
                                        'data': { 'role': 'Head', 'pos': 'Caa', 'term': '、', },
                                        'children': [],
                                    },
                                    {
                                        'id': 9,
                                        'data': { 'role': 'DUMMY2', 'pos': 'Naa', 'term': '午餐', },
                                        'children': [],
                                    },
                                ],
                            },
                            {
                                'id': 10,
                                'data': { 'role': 'Head', 'pos': 'Caa', 'term': '和', },
                                'children': [],
                            },
                            {
                                'id': 11,
                                'data': { 'role': 'DUMMY2', 'pos': 'Nab', 'term': '晚餐', },
                                'children': [],
                            },
                        ],
                    },
                ],
            },
            {
                'id': 12,
                'data': { 'role': 'quantity', 'pos': 'Dab', 'term': '都', },
                'children': [],
            },
            {
                'id': 13,
                'data': { 'role': 'target', 'pos': 'PP', 'term': None, },
                'children': [
                    {
                        'id': 14,
                        'data': { 'role':  'Head', 'pos': 'P30', 'term': '往', },
                        'children': [],
                    },
                    {
                        'id': 15,
                        'data': { 'role':  'DUMMY', 'pos': 'NP', 'term': None, },
                        'children': [
                            {
                                'id': 16,
                                'data': { 'role':  'property', 'pos': 'Ncb', 'term': '天', },
                                'children': [],
                            },
                            {
                                'id': 17,
                                'data': { 'role':  'Head', 'pos': 'Ncda', 'term': '上', },
                                'children': [],
                            },
                        ],
                    },
                ],
            },
            {
                'id': 18,
                'data': { 'role': 'Head', 'pos': 'VA11', 'term': '飛', },
                'children': [],
            },
            {
                'id': 19,
                'data': { 'role': 'aspect', 'pos': 'Di', 'term': '了', },
                'children': [],
            },
        ],
    }

    def _assertEqual(self, obj):
        self.assertEqual(len(obj), 20)
        self._assertEqualNode(obj, 0, None, None, 'S', None)
        self._assertEqualNode(obj, 1, 0, 'theme', 'NP', None)
        self._assertEqualNode(obj, 2, 1, 'possessor', 'N‧的', None)
        self._assertEqualNode(obj, 3, 2, 'head', 'Nhaa', '我')
        self._assertEqualNode(obj, 4, 2, 'Head', 'DE', '的')
        self._assertEqualNode(obj, 5, 1, 'Head', 'Nab', None)
        self._assertEqualNode(obj, 6, 5, 'DUMMY1', 'Nab', None)
        self._assertEqualNode(obj, 7, 6, 'DUMMY1', 'Nab', '早餐')
        self._assertEqualNode(obj, 8, 6, 'Head', 'Caa', '、')
        self._assertEqualNode(obj, 9, 6, 'DUMMY2', 'Naa', '午餐')
        self._assertEqualNode(obj, 10, 5, 'Head', 'Caa', '和')
        self._assertEqualNode(obj, 11, 5, 'DUMMY2', 'Nab', '晚餐')
        self._assertEqualNode(obj, 12, 0, 'quantity', 'Dab', '都')
        self._assertEqualNode(obj, 13, 0, 'target', 'PP', None)
        self._assertEqualNode(obj, 14, 13, 'Head', 'P30', '往')
        self._assertEqualNode(obj, 15, 13, 'DUMMY', 'NP', None)
        self._assertEqualNode(obj, 16, 15, 'property', 'Ncb', '天')
        self._assertEqualNode(obj, 17, 15, 'Head', 'Ncda', '上')
        self._assertEqualNode(obj, 18, 0, 'Head', 'VA11', '飛')
        self._assertEqualNode(obj, 19, 0, 'aspect', 'Di', '了')

    def _assertEqualNode(self, obj, node_id, parent_id, role, pos, term):
        node = obj[node_id]
        node_data = node.data
        if parent_id is not None:
            self.assertEqual(obj.parent(node_id).identifier, parent_id)
        else:
            self.assertEqual(obj.parent(node_id), None)
        self.assertEqual(node.tag, node_data.to_text())
        self.assertEqual(node_data.role, role)
        self.assertEqual(node_data.pos, pos)
        self.assertEqual(node_data.term, term)

    def test_normalize_text(self):
        text_orig = '#1:1.[0] ' + self.text_in + '#'
        text_out = self.obj_class.normalize_text(text_orig)
        self.assertEqual(text_out, self.text_in)

    def test_get_heads(self):
        obj = self.obj_class.from_text(self.text_in)
        self._assertGetHeads(obj, 0, [18])
        self._assertGetHeads(obj, 1, [7, 9, 11])
        self._assertGetHeads(obj, 2, [3])
        self._assertGetHeads(obj, 13, [17])

    def _assertGetHeads(self, obj, node_id, heads_id):
        heads_id_out = [node.identifier for node in obj.get_heads(node_id)]
        self.assertEqual(heads_id_out, heads_id)

    def test_get_relations(self):
        obj = self.obj_class.from_text(self.text_in)
        rels_id = {
            (7, 3, 'possessor',),
            (9, 3, 'possessor',),
            (11, 3, 'possessor',),
            (17, 16, 'property',),
            (18, 11, 'theme',),
            (18, 12, 'quantity',),
            (18, 17, 'target',),
            (18, 19, 'aspect',),
            (18, 7, 'theme',),
            (18, 9, 'theme',),
        }
        rels_id_out = {(rel.head.identifier, rel.tail.identifier, rel.relation) for rel in obj.get_relations()}
        self.assertEqual(rels_id_out, rels_id)
