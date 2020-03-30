#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides base drivers.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from ckipnlp.util.logger import (
    get_logger as _get_logger
)

################################################################################################################################

class BaseDriver:  # pylint: disable=too-few-public-methods
    """The base CKIPNLP driver."""

    def __init__(self):
        _get_logger().info(f'Initializing {self.__class__.__name__} ...')
