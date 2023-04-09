#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2023 CKIP Lab'
__license__ = 'GPL-3.0'

import abc
import json

################################################################################################################################

class _TestBase(metaclass=abc.ABCMeta):

    obj_class = NotImplemented
    text_in = NotImplemented

    @property
    def list_in(self):
        return self.text_in

    @property
    def dict_in(self):
        return self.list_in

    @property
    def json_in(self):
        return json.dumps(self.dict_in, ensure_ascii=False)

    @abc.abstractmethod
    def _assert_body(self, obj):
        return NotImplemented

    def _assert_iterable(self, obj1, obj2):
        assert [*obj1] == [*obj2]

    def test_io_text(self):
        obj = self.obj_class.from_text(self.text_in)
        assert isinstance(obj, self.obj_class)
        self._assert_body(obj)
        text_out = obj.to_text()
        assert text_out == self.text_in

    def test_io_list(self):
        obj = self.obj_class.from_list(self.list_in)
        assert isinstance(obj, self.obj_class)
        self._assert_body(obj)
        list_out = obj.to_list()
        assert list_out == self.list_in

    def test_io_dict(self):
        obj = self.obj_class.from_dict(self.dict_in)
        assert isinstance(obj, self.obj_class)
        self._assert_body(obj)
        dict_out = obj.to_dict()
        assert dict_out == self.dict_in

    def test_io_json(self):
        obj = self.obj_class.from_json(self.json_in)
        assert isinstance(obj, self.obj_class)
        self._assert_body(obj)
        json_out = obj.to_json(ensure_ascii=False)
        assert json_out == self.json_in
