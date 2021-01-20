#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module implements CKIPNLP pipelines.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

from .kernel import (
    CkipPipeline,
    CkipDocument,
)

from .coref import (
    CkipCorefPipeline,
    CkipCorefDocument,
)
