#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module implements data loading utilities for CKIPNLP.
"""

# pylint: disable=missing-docstring

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

import os as _os
import shutil as _shutil

from abc import (
    ABCMeta as _ABCMeta,
    abstractmethod as _abstractmethod,
)

from appdirs import (
    AppDirs as _AppDirs,
)

from ckipnlp.util.logger import (
    get_logger as _get_logger
)

_ROOTDIRS = _AppDirs(appname='ckipnlp', appauthor='ckip')

################################################################################################################################

class _DataBase(metaclass=_ABCMeta):

    name = NotImplemented
    fullname = NotImplemented
    env = NotImplemented
    extra_dirs = ()

    @classmethod
    def env_data_dir(cls):
        return _os.getenv(cls.env)  # pylint: disable=invalid-envvar-value

    @classmethod
    def user_data_dir(cls):
        return _os.path.join(_ROOTDIRS.user_data_dir, cls.name)

    @classmethod
    def site_data_dir(cls):
        return _os.path.join(_ROOTDIRS.user_data_dir, cls.name)

    @classmethod
    def get_data(cls):
        for data_dir in (
            cls.env_data_dir(),
            cls.user_data_dir(),
            cls.site_data_dir(),
            *cls.extra_dirs,
        ):
            if data_dir and _os.path.isdir(data_dir):
                break
        else:
            _get_logger().warning(f'No existing data for {cls.fullname}. Download data from remote ...')
            data_dir = cls.download_data()
        return data_dir

    @classmethod
    def install_data(cls, src_dir, *, copy=False):
        data_dir = cls.user_data_dir()

        if _os.path.isdir(data_dir):
            _get_logger().warning(f'{data_dir} already exists!')

        else:
            _os.makedirs(_os.path.dirname(data_dir), exist_ok=True)
            if not copy:
                _get_logger().debug(f'Linking CkipTagger data from {src_dir} to {data_dir} ...')
                _os.symlink(src_dir, data_dir)
                _get_logger().debug(f'Linking CkipTagger data from {src_dir} to {data_dir} ... done')
            else:
                _get_logger().debug(f'Copying CkipTagger data from {src_dir} to {data_dir} ...')
                _shutil.copytree(src_dir, data_dir)
                _get_logger().debug(f'Copying CkipTagger data from {src_dir} to {data_dir} ... done')

        return data_dir

    @classmethod
    def download_data(cls):
        data_dir = cls.user_data_dir()
        _get_logger().debug(f'Downloading CkipTagger data to {data_dir} ...')
        cls._download_data(data_dir)
        _get_logger().debug(f'Downloading CkipTagger data to {data_dir} ... done')
        return data_dir

    @classmethod
    @_abstractmethod
    def _download_data(cls, data_dir):
        return NotImplemented


################################################################################################################################

class TaggerData(_DataBase):

    name = 'tagger'
    fullname = 'CkipTagger'
    env = 'CKIPTAGGER_DATA'
    extra_dirs = ('./data',)

    @classmethod
    def user_data_dir(cls):
        return _os.path.join(super().user_data_dir(), 'data')

    @classmethod
    def site_data_dir(cls):
        return _os.path.join(super().site_data_dir(), 'data')

    @classmethod
    def _download_data(cls, data_dir):
        data_dir = super().user_data_dir()
        from ckiptagger.data_utils import download_data_url
        _os.makedirs(data_dir, exist_ok=True)
        download_data_url(data_dir)

# pylint: disable=invalid-name
get_tagger_data = TaggerData.get_data            #: Get CkipTagger data directory.
install_tagger_data = TaggerData.install_data    #: Link/Copy CkipTagger data directory.
download_tagger_data = TaggerData.download_data  #: Download CkipTagger data directory.
