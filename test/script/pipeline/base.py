#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

try:
    import os
    import tensorflow as tf
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    tf.logging.set_verbosity(tf.logging.ERROR)
except:
    pass

from ckipnlp.pipeline import *
from ckipnlp.driver import *
from ckipnlp.container import *

################################################################################################################################

raw = '中文字耶，啊哈哈哈。\n「完蛋了！」畢卡索他想'
text = [
    '中文字耶，啊哈哈哈。',
    '「完蛋了！」畢卡索他想',
]
ws = [
    [ '中文字', '耶', '，', '啊', '哈', '哈哈', '。', ],
    [ '「', '完蛋', '了', '！', '」', '畢卡索', '他', '想', ],
]
pos = [
    [ 'Na', 'T', 'COMMACATEGORY', 'I', 'D', 'D', 'PERIODCATEGORY', ],
    [ 'PARENTHESISCATEGORY', 'VH', 'T', 'EXCLAMATIONCATEGORY', 'PARENTHESISCATEGORY', 'Nb', 'Nh', 'VE', ],
]
ner = [
    [ [ '中文字', 'LANGUAGE', (0, 3), ], ],
    [ [ '畢卡索', 'PERSON', (6, 9), ], ],
]
constituency = [
    [
        [ 'S(Head:Nab:中文字|particle:Td:耶)', '，', ],
        [ '%(particle:I:啊|manner:Dh:哈|manner:D:哈哈)', '。', ],
    ],
    [
        [ None, '「', ],
        [ 'VP(Head:VH11:完蛋|particle:Ta:了)', '！」', ],
        [ 'S(agent:NP(apposition:Nba:畢卡索|Head:Nhaa:他)|Head:VE2:想)', '', ],
    ],
]