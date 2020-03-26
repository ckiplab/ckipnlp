#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import abc
import json
import unittest

################################################################################################################################

class _TestCaseBase(metaclass=abc.ABCMeta):

    obj_class = NotImplemented
    text_in = NotImplemented
    dict_in = NotImplemented

    @property
    def list_in(self):
        return self.dict_in

    @property
    def json_in(self):
        return json.dumps(self.dict_in, ensure_ascii=False)

    @abc.abstractmethod
    def _assertEqual(self, obj):
        return NotImplemented

    def test_io_text(self):
        obj = self.obj_class.from_text(self.text_in)
        self._assertEqual(obj)
        text_out = obj.to_text()
        self.assertEqual(text_out, self.text_in)

    def test_io_dict(self):
        obj = self.obj_class.from_dict(self.dict_in)
        self._assertEqual(obj)
        dict_out = obj.to_dict()
        self.assertEqual(dict_out, self.dict_in)

    def test_io_list(self):
        obj = self.obj_class.from_list(self.list_in)
        self._assertEqual(obj)
        list_out = obj.to_list()
        self.assertEqual(list_out, self.list_in)

    def test_io_json(self):
        obj = self.obj_class.from_json(self.json_in)
        self._assertEqual(obj)
        json_out = obj.to_json(ensure_ascii=False)
        self.assertEqual(json_out, self.json_in)
