#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import os as _os
import warnings as _warnings

try:
    if not _os.environ.get('_SPHINX'):
        from ckipnlp._core.parser import CkipParserCore
except ImportError as exc:
    raise ImportError(
        'Please reinstall ‘ckipnlp’ with ‘--install-option=\'--parser\'’.  --install-option=\'--parser-dir=<...>\''
        'Visit https://pypi.org/project/ckipnlp for more information.'
    ) from exc
except Exception as exc:
    raise exc

from ckipnlp.util.ini import create_ws_lex, create_ws_ini, create_parser_ini

class CkipParser:
    """The CKIP sentence parsing driver.

    Parameters
    ----------
        logger : bool
            enable logger.
        lex_list : Iterable
            passed to :meth:`ckipnlp.util.ini.create_ws_lex`,
            overridden **lex_file** for :meth:`ckipnlp.util.ini.create_ws_ini`.
        ini_file : str
            the path to the INI file.
        ws_ini_file : str
            the path to the INI file for CKIPWS.

    Other Parameters
    ----------------
        **
            the configs for CKIPParser, passed to :meth:`ckipnlp.util.ini.create_parser_ini`, ignored if **ini_file** is set.
        **
            the configs for CKIPWS, passed to :meth:`ckipnlp.util.ini.create_ws_ini`, ignored if **ws_ini_file** is set.

    .. danger::
        Never instance more than one object of this class!
    """

    def __init__(self, *,
        logger=False,
        ini_file=None,
        ws_ini_file=None,
        lex_list=None,
        **kwargs,
    ):

        self.__core = CkipParserCore()

        if logger:
            # self.__core.enable_logger()
            _warnings.warn('Logger is not supported for CKIP Parser')

        if lex_list:
            lex_file, f_lex = create_ws_lex(*lex_list)
            kwargs['lex_file'] = lex_file

        if not ws_ini_file:
            ws_ini_file, f_ws_ini, kwargs = create_ws_ini(**kwargs)

        if not ini_file:
            ini_file, f_ini, kwargs = create_parser_ini(ws_ini_file=ws_ini_file, **kwargs)

        def CkipParser(*, _=None): pass # pylint: disable=redefined-outer-name, invalid-name, multiple-statements
        CkipParser(**kwargs)

        self.__core.init_data(ini_file)

        try:
            f_lex.close()
        except: # pylint: disable=bare-except
            pass

        try:
            f_ws_ini.close()
        except: # pylint: disable=bare-except
            pass

        try:
            f_ini.close()
        except: # pylint: disable=bare-except
            pass

    @staticmethod
    def normalize_text(text):
        """Text normalization output.

        Replacing keywords ``()+-:|&#`` by by full-width ones.
        """
        return (text
            .replace('(', '（')
            .replace(')', '）')
            .replace('+', '＋')
            .replace('-', '－')
            .replace(':', '：')
            .replace('|', '｜')
            .replace('&', '＆') # for tree draw
            .replace('#', '＃') # for tree draw
        )

    def __call__(self, text):
        return self.apply(text)

    def apply(self, text, *, normalize=True):
        """Parse a sentence.

        Parameters
        ----------
            text : str
                the input sentence.
            normalize : bool
                do text normalization (please refer :meth:`normalize_text`).

        Return
        ------
            str
                the output sentence.

        .. hint::
            One may also call this method as :meth:`__call__`.
        """
        return self.apply_list([text], normalize=normalize)[0]

    def apply_list(self, ilist, *, normalize=True):
        """Parse a list of sentences.

        Parameters
        ----------
            ilist : List[str]
                the list of input sentences.
            normalize : bool
                do text normalization (please refer :meth:`normalize_text`).

        Return
        ------
            List[str]
                the list of output sentences.
        """
        if normalize:
            ilist = list(map(self.normalize_text, ilist))
        return self.__core.apply_list(ilist)

    def apply_file(self, ifile, ofile):
        """Parse a file.

        Parameters
        ----------
            ifile : str
                 the input file.
            ofile : str
                 the output file (will be overwritten).
        """
        return self.__core.apply_file(ifile, ofile)
