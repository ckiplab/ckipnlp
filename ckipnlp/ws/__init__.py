#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__    = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2018-2019'

try:
    from ckipnlp._core.ws import CkipWSCore
except ImportError:
    raise ImportError(
        'Please reinstall "ckipnlp" with "--install-option=\'--ws\'". '
        'Visit https://pypi.org/project/ckipnlp for more information.',
    )

import tempfile as _tempfile

from ckipnlp.util.ini import create_ws_ini

class CkipWS:
    """The CKIP word segmentation driver.

    Args:
        logger (bool): enable logger.
        inifile (str): the path to the INI file.
        options:       the options (see :func:`ckipnlp.util.ini.create_ws_ini`).
    """

    def __init__(self, *, logger=False, inifile=None, **options):

        self.__core = CkipWSCore()

        if logger:
            self.__core.enable_logger()

        if not inifile:
            fini = _tempfile.NamedTemporaryFile(mode='w')
            inifile = fini.name
            inidata, options = create_ws_ini(**options)
            fini.write(inidata)
            fini.flush()

        def CkipWS(*, _=None): return None
        CkipWS(**options)

        self.__core.init_data(inifile)

        try:
            fini.close()
        except:
            pass

    def __call__(self, text):
        """Segment a sentence.

        Args:
            text (str): the input sentence.

        Return:
            str:        the output sentence.
        """
        return self.__core.apply_list([text])[0]

    def apply_list(self, ilist):
        """Segment a list of sentences.

        Args:
            ilist (list): the list of input sentences (str).

        Return:
            list:         the list of output sentences (str).
        """
        return self.__core.apply_list(ilist)

    def apply_file(self, ifile, ofile, uwfile=''):
        """Segment a file.

        Args:
            ifile (str):  the input file.
            ofile (str):  the output file (will be overwritten).
            uwfile (str): the unknown word file (will be overwritten).
        """
        return self.__core.apply_file(ifile, ofile, uwfile)
