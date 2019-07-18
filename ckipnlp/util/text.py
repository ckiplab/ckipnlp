#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2018-2019'

def ws_split(sentence):
    return [word.strip(')').rsplit('(', 1) for word in sentence.split('\u3000')]
