#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2018-2019'

import os as _os
import tempfile as _tempfile
import warnings as _warnings

try:
    if not _os.environ.get('_SPHINX'):
        from ckipnlp._core.ws import CkipWsCore
except ImportError as exc:
    raise ImportError(
        'Please reinstall ‘ckipnlp’ with ‘--install-option=\'--ws\'’. '
        'Visit https://pypi.org/project/ckipnlp for more information.'
    ) from exc
except Exception as exc:
    raise exc

from ckipnlp.util.ini import create_ws_ini

class CkipWs:
    """The CKIP word segmentation driver.

    Parameters
    ----------
    logger : bool
        enable logger.
    inifile : str
        the path to the INI file.
    options:
        the options, see :func:`ckipnlp.util.ini.create_ws_ini`.
    """

    def __init__(self, *, logger=False, inifile=None, **options):

        self.__core = CkipWsCore()

        if logger:
            self.__core.enable_logger()

        if not inifile:
            fini = _tempfile.NamedTemporaryFile(mode='w')
            inifile = fini.name
            inidata, options = create_ws_ini(**options)
            fini.write(inidata)
            fini.flush()

        def CkipWs(*, _=None): pass # pylint: disable=redefined-outer-name, invalid-name, multiple-statements
        CkipWs(**options)

        self.__core.init_data(inifile)

        try:
            fini.close()
        except: # pylint: disable=bare-except
            pass

    def __call__(self, text):
        return self.apply(text)

    def apply(self, text):
        """Segment a sentence.

        Parameters
        ----------
        text : str
            the input sentence.

        Return
        ------
        str
            the output sentence.

        Notes
        -----
        One may also call this method as :func:`__call__`.
        """
        return self.apply_list([text])[0]

    def apply_list(self, ilist):
        """Segment a list of sentences.

        Parameters
        ----------
        ilist: list
            the list of input sentences (str).

        Return
        ------
        olist: list
            the list of output sentences (str).
        """
        return self.__core.apply_list(ilist)

    def apply_file(self, ifile, ofile, uwfile=''):
        """Segment a file.

        Parameters
        ----------
        ifile: str
             the input file.
        ofile: str
             the output file (will be overwritten).
        uwfile: str
            the unknown word file (will be overwritten).
        """
        return self.__core.apply_file(ifile, ofile, uwfile)
