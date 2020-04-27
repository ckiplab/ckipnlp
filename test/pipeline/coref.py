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

raw = '畢卡索他想，完蛋了'
coref = [
    [
        [ '畢卡索', (0, 'source'), 2, ],
        [ '他', (0, 'target'), 3, ],
        [ '想', None, 4, ],
    ],
    [
        [ None, (0, 'zero'), None, ],
        [ '完蛋', None, 1, ],
        [ '了', None, 2, ],
    ],
]

################################################################################################################################

class TestCorefChunker(unittest.TestCase):

    def test(self):
        obj = CkipCorefPipeline()
        doc = CkipDocument(raw=raw)
        corefdoc = obj(doc)
        self.assertSequenceEqual(corefdoc.coref.to_list(), coref)
