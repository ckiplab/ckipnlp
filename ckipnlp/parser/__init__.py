#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2018-2019'

try:
    from ckipnlp._core.parser import CkipParserCore
except ImportError:
    raise ImportError(
        'Please reinstall "ckipnlp" with "--install-option=\'--parser\'". '
        'Visit https://pypi.org/project/ckipnlp for more information.',
    )

import tempfile as _tempfile
import warnings as _warnings

from ckipnlp.util.ini import create_ws_ini, create_parser_ini

class CkipParser:
    """The CKIP sentence parsing driver.

    Args:
        logger (bool):   enable logger.
        inifile (str):   the path to the INI file.
        wsinifile (str): the path to the INI file for CKIPWS.
        options:         the options (see :func:`ckipnlp.util.ini.create_ws_ini`
                                      and :func:`ckipnlp.util.ini.create_parser_ini`).
    """

    def __init__(self, *, logger=False, inifile=None, wsinifile=None, **options):

        self.__core = CkipParserCore()

        if logger:
            # self.__core.enable_logger()
            _warnings.warn('Logger is not supported for CKIP Parser')

        if not wsinifile:
            fwsini = _tempfile.NamedTemporaryFile(mode='w')
            wsinifile = fwsini.name
            wsinidata, options = create_ws_ini(**options)
            fwsini.write(wsinidata)
            fwsini.flush()

        if not inifile:
            fini = _tempfile.NamedTemporaryFile(mode='w')
            inifile = fini.name
            inidata, options = create_parser_ini(wsinifile=wsinifile, **options)
            fini.write(inidata)
            fini.flush()

        def CkipParser(*, _=None): pass # pylint: disable=redefined-outer-name, invalid-name, multiple-statements
        CkipParser(**options)

        self.__core.init_data(inifile)

        try:
            fwsini.close()
        except: # pylint: disable=bare-except
            pass

        try:
            fini.close()
        except: # pylint: disable=bare-except
            pass

    def __call__(self, text):
        """Segment a sentence.

        Args:
            text (str): the input sentence.

        Return:
            str:        the output sentence.
        """
        return self.apply_list([text])[0]

    def apply_list(self, ilist):
        """Segment a list of sentences.

        Args:
            ilist (list): the list of input sentences (str).

        Return:
            list:         the list of output sentences (str).
        """
        return self.__core.apply_list(ilist)

    def apply_file(self, ifile, ofile):
        """Segment a file.

        Args:
            ifile (str): the input file.
            ofile (str): he output file (will be overwritten).
        """
        return self.__core.apply_file(ifile, ofile)
