#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

# pylint: disable=too-many-lines

__all__ = [
    '_SUBJECT_ROLES',
    '_OBJECT_ROLES',
    '_NEUTRAL_ROLES',
    '_HUMAN_WORDS',
    '_PRONOUN_WORDS',
]

_SUBJECT_ROLES = {'agent', 'causer', 'experiencer'}
_OBJECT_ROLES = {'benefactor', 'companion', 'comparison', 'goal', 'range', 'source', 'target'}
_NEUTRAL_ROLES = {'theme', 'topic'}

from .human_words import _HUMAN_WORDS
from .pronoun_words import _PRONOUN_WORDS
