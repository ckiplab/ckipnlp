#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import os
import unittest

from ckipnlp.pipeline import *
from ckipnlp.container import *

################################################################################################################################

import tensorflow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

################################################################################################################################

raw = '「完蛋了！」畢卡索他想\n但是也沒有辦法'
coref = [
    [
        [ '「', None, (0, None), ],
        [ '完蛋', None, (1, 1), ],
        [ '了', None, (1, 2), ],
        [ '！」', None, (1, None), ],
        [ '畢卡索', (0, 'source'), (2, 2), ],
        [ '他', (0, 'target'), (2, 3), ],
        [ '想', None, (2, 4), ],
    ],
    [
        [ '但是', None, (0, 1), ],
        [ None, (0, 'zero'), (0, None), ],
        [ '也', None, (0, 2), ],
        [ '沒有', None, (0, 3), ],
        [ '辦法', None, (0, 5), ],
    ],
]

################################################################################################################################

class TestCorefChunker(unittest.TestCase):

    def test(self):
        obj = CkipCorefPipeline()
        doc = CkipDocument(raw=raw)
        corefdoc = obj(doc)
        list_out = corefdoc.coref.to_list()

        self.assertEqual(len(list_out), len(coref))
        for i in range(len(coref)):
            self.assertSequenceEqual(list_out[i], coref[i])
