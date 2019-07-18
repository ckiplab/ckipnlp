#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2018-2019'

def ws_split(text):
    """Split CkipWS output into a list of words and post-tags.

        Args:
            text (str): the input sentence from CkipWS output.

        Return:
            list:       (word, post-tag,) pairs.

    """
    return [word.strip(')').rsplit('(', 1) for word in text.split('\u3000')]
