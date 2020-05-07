#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module implements CKIPNLP drivers.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from .base import (
    DriverType,
    DriverFamily,
)

from .tagger import (
    CkipTaggerWordSegmenter,
    CkipTaggerPosTagger,
    CkipTaggerNerChunker,
)

from .classic import (
    CkipClassicWordSegmenter,
    CkipClassicSentenceParser,
)

from .ss import (
    CkipSentenceSegmenter,
)

from .coref import (
    CkipCorefChunker,
)
