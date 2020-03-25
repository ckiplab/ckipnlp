#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides base drivers.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

################################################################################################################################

class BaseDriver:
    """The base CKIPNLP driver."""

    def __init__(self):
        print(f'Initializing {self.__class__.__name__} ...')

    def __call__(self, **kwargs):
        print(f'Calling {self.__class__.__name__} ...')
        return f'<{self.__class__.__name__} {kwargs}>'
        # raise NotImplementedError
