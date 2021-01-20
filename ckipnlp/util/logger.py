#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module implements logging utilities for CKIPNLP.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

import logging as _logging

################################################################################################################################

def get_logger():
    """Get the CKIPNLP logger."""
    return _logging.getLogger('ckipnlp')
