#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import json
import unittest

from .base import _TestCaseBase
from ckipnlp.container.parsed import *

################################################################################################################################

class TestParsedSentenceList(unittest.TestCase, _TestCaseBase):

    obj_class = ParsedSentenceList

    text_in = [
        '#1:1.[0] S(Head:Nab:中文字|particle:Td:耶)#',
        '#2:1.[0] %(particle:I:啊|manner:Dh:哈|manner:Dh:哈|time:Dh:哈)#',
    ]

    def _assertEqual(self, obj):
        self.assertEqual(len(obj), 2)
        self.assertEqual(obj[0], self.text_in[0])
        self.assertEqual(obj[1], self.text_in[1])
