#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# pylint: disable=missing-docstring

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

################################################################################################################################

SUBJECT_ROLES = {'agent', 'causer', 'experiencer'}
OBJECT_ROLES = {'benefactor', 'companion', 'comparison', 'goal', 'range', 'source', 'target'}
NEUTRAL_ROLES = {'theme', 'topic'}
APPOSITION_ROLES = {'apposition'}

HUMAN_ROLES = {
    *SUBJECT_ROLES,
    *OBJECT_ROLES,
    *NEUTRAL_ROLES,
    *APPOSITION_ROLES,
}
