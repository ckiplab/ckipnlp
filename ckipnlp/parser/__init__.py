#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2019 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import os as _os
import tempfile as _tempfile
import warnings as _warnings

try:
    if not _os.environ.get('_SPHINX'):
        from ckipnlp._core.parser import CkipParserCore
except ImportError as exc:
    raise ImportError(
        'Please reinstall ‘ckipnlp’ with ‘--install-option=\'--parser\'’. '
        'Visit https://pypi.org/project/ckipnlp for more information.'
    ) from exc
except Exception as exc:
    raise exc

from ckipnlp.util.ini import create_ws_ini, create_parser_ini

class CkipParser:
    """The CKIP sentence parsing driver.

    Parameters
    ----------
        logger : bool
            enable logger.
        inifile : str
            the path to the INI file.
        wsinifile : str
            the path to the INI file for CKIPWS.
    Other Parameters
    ----------------
        **
            the configs for CKIPParser, ignored if **inifile** is set. Please refer :func:`ckipnlp.util.ini.create_parser_ini`.
        **
            the configs for CKIPWS, ignored if **wsinifile** is set. Please refer :func:`ckipnlp.util.ini.create_ws_ini`.

    Warning
    -------
        Never instance more than one object of this class!
    """

    def __init__(self, *,
        logger=False,
        inifile=None,
        wsinifile=None,
        **kwargs,
    ):

        self.__core = CkipParserCore()

        if logger:
            # self.__core.enable_logger()
            _warnings.warn('Logger is not supported for CKIP Parser')

        if not wsinifile:
            fwsini = _tempfile.NamedTemporaryFile(mode='w')
            wsinifile = fwsini.name
            wsinidata, kwargs = create_ws_ini(**kwargs)
            fwsini.write(wsinidata)
            fwsini.flush()

        if not inifile:
            fini = _tempfile.NamedTemporaryFile(mode='w')
            inifile = fini.name
            inidata, kwargs = create_parser_ini(wsinifile=wsinifile, **kwargs)
            fini.write(inidata)
            fini.flush()

        def CkipParser(*, _=None): pass # pylint: disable=redefined-outer-name, invalid-name, multiple-statements
        CkipParser(**kwargs)

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

        .. note::
            One may also call this method as :func:`__call__`.
        """
        return self.apply_list([text])[0]

    def apply_list(self, ilist):
        """Segment a list of sentences.

        Parameters
        ----------
            ilist
                the list of input sentences.

        Return
        ------
            List[str]
                the list of output sentences.
        """
        return self.__core.apply_list(ilist)

    def apply_file(self, ifile, ofile):
        """Segment a file.

        Parameters
        ----------
            ifile : str
                 the input file.
            ofile : str
                 the output file (will be overwritten).
        """
        return self.__core.apply_file(ifile, ofile)
