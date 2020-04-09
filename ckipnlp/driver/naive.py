#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import re as _re

from ckipnlp.container import (
    TextParagraph as _TextParagraph,
)

from .base import (
    BaseDriver as _BaseDriver
)

################################################################################################################################

class CkipNaiveSentenceSegmenter(_BaseDriver):  # pylint: disable=too-few-public-methods
    """The CKIP sentence-segmentation driver.

    Do sentence-segmentation based on punctuations.

    """

    def __init__(self, *, delims=',，。!！?？:：;；\n'):
        super().__init__()

        self.delims = delims

    def __call__(self, *, raw, keep_delim=False):
        assert isinstance(raw, str)

        if not keep_delim:
            text = _re.split(rf'[{self.delims}]+', raw)
        else:
            text = _re.split(rf'([{self.delims}]+)', raw)
            if text[-1] == '':
                del text[-1]
            if len(text) % 2:
                text.append('')
            text = [word+punct for word, punct in zip(text[::2], text[1::2])]

        return _TextParagraph.from_text(text)
