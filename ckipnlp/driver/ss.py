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
    BaseDriver as _BaseDriver,
    DriverType as _DriverType,
    DriverKind as _DriverKind,
)

################################################################################################################################

class CkipSentenceSegmenter(_BaseDriver): # pylint: disable=too-few-public-methods
    """The CKIP sentence segmentation driver."""

    driver_type = _DriverType.SENTENCE_SEGMENTER
    driver_kind = _DriverKind.BUILTIN

    def __init__(self, *, delims=',，。!！?？:：;；\n', lazy=False):
        super().__init__(lazy=lazy)

        self.delims = delims

    def _init(self):
        pass

    def _call(self, *, raw, keep_all=False):
        assert isinstance(raw, str)

        if not keep_all:
            # Replace spaces
            text = _re.sub(rf'[^\S{self.delims}]', '', raw)

            # Segment
            text = _re.split(rf'[{self.delims}]+', text)

            # Remove empty lines
            text = filter(None, text)

        else:
            text = _re.split(rf'([{self.delims}]+)', raw)
            if text[-1] == '':
                del text[-1]
            if len(text) % 2:
                text.append('')
            text = [word+punct for word, punct in zip(text[::2], text[1::2])]

        return _TextParagraph.from_text(text)
