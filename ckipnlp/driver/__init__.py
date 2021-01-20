#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module implements CKIPNLP drivers.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

from .tagger import (
    CkipTaggerWordSegmenter,
    CkipTaggerPosTagger,
    CkipTaggerNerChunker,
)

from .classic import (
    CkipClassicWordSegmenter,
    CkipClassicConParser,
    CkipClassicConParserClient,
)

from .ss import (
    CkipSentenceSegmenter,
)

from .coref import (
    CkipCorefChunker,
)
