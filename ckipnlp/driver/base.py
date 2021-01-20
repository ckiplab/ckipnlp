#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides base drivers.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

from abc import (
    ABCMeta as _ABCMeta,
    abstractmethod as _abstractmethod,
)

from ckipnlp.util.logger import (
    get_logger as _get_logger,
)

################################################################################################################################

class DriverRegister:
    """The driver registering utility."""

    _DRIVERS = {}

    @staticmethod
    def get(driver_type, driver_family):  # pylint: disable=missing-docstring
        if driver_family is None:
            return DummyDriver

        driver = DriverRegister._DRIVERS.get((driver_type, driver_family,))
        if not driver:
            raise KeyError(f'{driver_type} is not implemented for type {driver_family}')
        if not driver.is_dummy:
            _get_logger().debug(f'Use {driver.__name__} ...')

        return driver

################################################################################################################################

class BaseDriver(metaclass=_ABCMeta):
    """The base CKIPNLP driver."""

    is_dummy = False

    def __init__(self, *, lazy=False):
        self._core = None
        self._inited = False

        if not lazy:
            self.init()

    def init(self):  # pylint: disable=missing-docstring
        if self._inited:
            return
        _get_logger().info(f'Initializing {self.__class__.__name__} ...')
        self._init()
        self._inited = True

    def __call__(self, *args, **kwargs):
        self.init()
        return self._call(*args, **kwargs)

    ########################################################################################################################

    @_abstractmethod
    def driver_type(self):  # pylint: disable=missing-docstring
        return NotImplemented

    @_abstractmethod
    def driver_family(self):  # pylint: disable=missing-docstring
        return NotImplemented

    @_abstractmethod
    def driver_inputs(self):  # pylint: disable=missing-docstring
        return NotImplemented

    @_abstractmethod
    def _init(self):
        return NotImplemented

    @_abstractmethod
    def _call(self):
        return NotImplemented

    def _call_from_pipeline(self, pipeline, doc):
        return self.__call__(**{
            key: pipeline._get(key, doc) for key in self.driver_inputs  # pylint: disable=protected-access
        })

    ########################################################################################################################

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        driver_type = cls.driver_type
        driver_family = cls.driver_family

        key = (driver_type, driver_family,)
        assert key not in DriverRegister._DRIVERS, f'{key} already registered!'  # pylint: disable=protected-access
        DriverRegister._DRIVERS[key] = cls  # pylint: disable=protected-access

################################################################################################################################

class DummyDriver(BaseDriver):
    """The dummy driver."""

    driver_type = None
    driver_family = None
    driver_inputs = None
    is_dummy = True

    def __init__(self, *, lazy=False):
        super().__init__(lazy=lazy)
        self._inited = True

    def _init(self):
        pass

    def _call(self):
        raise NotImplementedError
