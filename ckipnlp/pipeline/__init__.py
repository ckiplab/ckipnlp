#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module implements CKIPNLP pipelines.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from ..driver.base import (
    DriverType,
    DriverFamily,
)

from .core import (
    CkipPipeline,
    CkipDocument,
)

from .coref import (
    CkipCorefPipeline,
    CkipCorefDocument,
)
