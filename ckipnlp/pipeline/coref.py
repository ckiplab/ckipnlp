#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from .core import (
    CkipCoreDocument as _CkipCoreDocument,
    CkipCorePipeline as _CkipCorePipeline,
)

################################################################################################################################

class CkipCorefDocument:  # pylint: disable=too-few-public-methods
    """The co-reference document"""

    # def __init__(self, *, **kwargs, coref=None):
    #     self._core = _CkipCoreDocument(**kwargs)
    #     self.coref = coref

class CkipCorefPipeline:  # pylint: disable=too-few-public-methods
    """The co-reference pipeline"""

    # def __init__(self, *, **kwargs):
    #     self._core = _CkipCorePipeline(**kwargs)
    #     self._coref_driver = None
