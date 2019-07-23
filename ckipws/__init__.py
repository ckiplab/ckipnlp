#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import warnings
warnings.warn('Module ‘ckipws’ is deprecated. Please import ‘ckipnlp.ws’ instead.', FutureWarning)
from ckipnlp.ws import *
from ckipnlp import __version__

class CkipWS(CkipWs):
    warnings.warn('Class ‘CkipWS’ is deprecated. Please use ‘CkipWs’ instead.', FutureWarning)
