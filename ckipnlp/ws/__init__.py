#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2019 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import os as _os
import tempfile as _tempfile
import warnings as _warnings

from typing import (
    List,
    NoReturn,
)

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
    logger
        enable logger.
    inifile
        the path to the INI file.
    options:
        the options, see :func:`ckipnlp.util.ini.create_ws_ini`.

    Warning
    -------
    Never instance more than one object of this class!
    """

    def __init__(self, *,
        logger: bool = False,
        inifile: str = None,
        **options,
    ) -> NoReturn:

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

    def __call__(self,
        text: str,
    ) -> str:
        return self.apply(text)

    def apply(self,
        text: str,
    ) -> str:
        """Segment a sentence.

        Parameters
        ----------
        text
            the input sentence.

        Return
        ------
            the output sentence.

        .. note::
            One may also call this method as :func:`__call__`.
        """
        return self.apply_list([text])[0]

    def apply_list(self, ilist: List[str]) -> List[str]:
        """Segment a list of sentences.

        Parameters
        ----------
        ilist
            the list of input sentences.

        Return
        ------
            the list of output sentences.
        """
        return self.__core.apply_list(ilist)

    def apply_file(self,
        ifile: str,
        ofile: str,
        uwfile: str = '',
    ) -> NoReturn:
        """Segment a file.

        Parameters
        ----------
        ifile
            the input file.
        ofile
            the output file (will be overwritten).
        uwfile
            the unknown word file (will be overwritten).
        """
        return self.__core.apply_file(ifile, ofile, uwfile)
