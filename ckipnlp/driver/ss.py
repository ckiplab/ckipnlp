#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides built-in sentence segmentation driver.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

import re as _re

from ckipnlp.container import (
    TextParagraph as _TextParagraph,
)

from .base import (
    BaseDriver as _BaseDriver,
)

################################################################################################################################

class CkipSentenceSegmenter(_BaseDriver):  # pylint: disable=too-few-public-methods
    """The CKIP sentence segmentation driver.

    Arguments
    ---------
        lazy : bool
            Lazy initialize the driver.
        delims : str
            The delimiters.
        keep_delims : bool
            Keep the delimiters.

    .. method:: __call__(*, raw, keep_all=True)

        Apply sentence segmentation.

        Parameters
            **raw** (*str*) — The raw text.

        Returns
            **text** (:class:`TextParagraph <ckipnlp.container.text.TextParagraph>`) — The sentences.
    """

    driver_type = 'sentence_segmenter'
    driver_family = 'default'
    driver_inputs = ('raw',)

    def __init__(self, *, lazy=False, delims='\n', keep_delims=False):
        super().__init__(lazy=lazy)

        self.delims = delims
        self._keep_delims = keep_delims

    def _init(self):
        pass

    def _call(self, *, raw):
        assert isinstance(raw, str)

        if not self._keep_delims:
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
