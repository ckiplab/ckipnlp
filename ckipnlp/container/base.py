#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides base containers.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

import json as _json

from abc import (
    ABCMeta as _ABCMeta,
    abstractmethod as _abstractmethod,
)

from collections import (
    UserList as _UserList,
)

################################################################################################################################

class Base(metaclass=_ABCMeta):
    """The base CKIPNLP container."""

    ########################################################################################################################

    @classmethod
    @_abstractmethod
    def from_text(cls, data):
        """Construct an instance from text format.

        Parameters
        ----------
            data : str
        """
        return NotImplemented  # pragma: no cover

    @_abstractmethod
    def to_text(self):
        """Transform to plain text.

        Returns
        -------
            str
        """
        return NotImplemented  # pragma: no cover

    ########################################################################################################################

    @classmethod
    @_abstractmethod
    def from_list(cls, data):
        """Construct an instance from python built-in containers."""
        return NotImplemented  # pragma: no cover

    @_abstractmethod
    def to_list(self):
        """Transform to python built-in containers."""
        return NotImplemented  # pragma: no cover

    ########################################################################################################################

    @classmethod
    @_abstractmethod
    def from_dict(cls, data):
        """Construct an instance from python built-in containers."""
        return NotImplemented  # pragma: no cover

    @_abstractmethod
    def to_dict(self):
        """Transform to python built-in containers."""
        return NotImplemented  # pragma: no cover

    ########################################################################################################################

    @classmethod
    def from_json(cls, data, **kwargs):
        """Construct an instance from JSON format.

        Parameters
        ----------
            data : str
                please refer :meth:`from_dict` for format details.
        """
        return cls.from_dict(_json.loads(data, **kwargs))

    def to_json(self, **kwargs):
        """Transform to JSON format.

        Returns
        -------
            str
        """
        return _json.dumps(self.to_dict(), **kwargs)

################################################################################################################################

class BaseTuple(Base, metaclass=_ABCMeta):
    """The base CKIPNLP tuple."""

    ########################################################################################################################

    @classmethod
    @_abstractmethod
    def from_text(cls, data):
        return NotImplemented  # pragma: no cover

    @_abstractmethod
    def to_text(self):
        return NotImplemented  # pragma: no cover

    ########################################################################################################################

    @classmethod
    def from_list(cls, data):
        """Construct an instance from python built-in containers.

        Parameters
        ----------
            data : list
        """
        return cls(*data)

    def to_list(self):
        """Transform to python built-in containers.

        Returns
        -------
            list
        """
        return list(self)

    ########################################################################################################################

    @classmethod
    def from_dict(cls, data):
        """Construct an instance from python built-in containers.

        Parameters
        ----------
            data : dict
        """
        return cls(**data)

    def to_dict(self):
        """Transform to python built-in containers.

        Returns
        -------
            dict
        """
        return dict(self._asdict())  # pylint: disable=no-member

################################################################################################################################

class _BaseList(Base, _UserList):
    """The base CKIPNLP list."""

    item_class = NotImplemented

    ########################################################################################################################

    @classmethod
    def from_text(cls, data):
        """Construct an instance from text format.

        Parameters
        ----------
            data : Sequence[str]
                list of texts as ``item_class.from_text`` input.
        """
        return cls(map(cls._item_from_text, data))  # pylint: disable=no-member

    def to_text(self):
        """Transform to plain text.

        Returns
        -------
            List[str]
        """
        return list(map(self._item_to_text, self))  # pylint: disable=no-member

    ########################################################################################################################

    @classmethod
    def from_list(cls, data):
        """Construct an instance from python built-in containers.

        Parameters
        ----------
            data : Sequence[Container]
                list of objects as ``item_class.from_list`` input.
        """
        return cls(map(cls._item_from_list, data))  # pylint: disable=no-member

    def to_list(self):
        """Transform to python built-in containers.

        Returns
        -------
            List[Container]
        """
        return list(map(self._item_to_list, self))  # pylint: disable=no-member

    ########################################################################################################################

    @classmethod
    def from_dict(cls, data):
        """Construct an instance from python built-in containers.

        Parameters
        ----------
            data : Sequence[Container]
                list of objects as ``item_class.from_dict`` input.
        """
        return cls(map(cls._item_from_dict, data))  # pylint: disable=no-member

    def to_dict(self):
        """Transform to python built-in containers.

        Returns
        -------
            List[Container]
        """
        return list(map(self._item_to_dict, self))  # pylint: disable=no-member

################################################################################################################################

class _BaseSentence(_BaseList):
    """The base CKIPNLP sentence."""

    @classmethod
    def from_text(cls, data):
        """Construct an instance from text format.

        Parameters
        ----------
            data : str
                words segmented by ``'\\u3000'``.
        """
        return cls(map(cls._item_from_text, data.split('\u3000')))  # pylint: disable=no-member

    def to_text(self):
        return '\u3000'.join(map(self._item_to_text, self))  # pylint: disable=no-member

################################################################################################################################

class _InterfaceItem:
    """Container has ckipnlp item class."""

    @classmethod
    def _item_from_text(cls, data):
        return cls.item_class.from_text(data)  # pylint: disable=no-member

    @classmethod
    def _item_to_text(cls, item):
        return cls.item_class.to_text(item)  # pylint: disable=no-member

    @classmethod
    def _item_from_list(cls, data):
        return cls.item_class.from_list(data)  # pylint: disable=no-member

    @classmethod
    def _item_to_list(cls, item):
        return cls.item_class.to_list(item)  # pylint: disable=no-member

    @classmethod
    def _item_from_dict(cls, data):
        return cls.item_class.from_dict(data)  # pylint: disable=no-member

    @classmethod
    def _item_to_dict(cls, item):
        return cls.item_class.to_dict(item)  # pylint: disable=no-member

################################################################################################################################

class _InterfaceBuiltInItem:
    @classmethod
    def _item_from_text(cls, data):
        return cls.item_class(data)  # pylint: disable=no-member

    @classmethod
    def _item_to_text(cls, item):
        return cls.item_class(item)  # pylint: disable=no-member

    @classmethod
    def _item_from_list(cls, data):
        return cls.item_class(data)  # pylint: disable=no-member

    @classmethod
    def _item_to_list(cls, item):
        return cls.item_class(item)  # pylint: disable=no-member

    @classmethod
    def _item_from_dict(cls, data):
        return cls.item_class(data)  # pylint: disable=no-member

    @classmethod
    def _item_to_dict(cls, item):
        return cls.item_class(item)  # pylint: disable=no-member

################################################################################################################################

class BaseList(_BaseList, _InterfaceItem):
    """The base CKIPNLP list.

    .. attribute:: item_class
        :value: Not Implemented

        Must be a CKIPNLP container class.
    """

class BaseList0(_BaseList, _InterfaceBuiltInItem):
    """The base CKIPNLP list with built-in item class.

    .. attribute:: item_class
        :value: Not Implemented

        Must be a built-in type.
    """

class BaseSentence(_BaseSentence, _InterfaceItem):
    """The base CKIPNLP sentence.

    .. attribute:: item_class
        :value: Not Implemented

        Must be a CKIPNLP container class.
    """

class BaseSentence0(_BaseSentence, _InterfaceBuiltInItem):
    """The base CKIPNLP sentence with built-in item class.

    .. attribute:: item_class
        :value: Not Implemented

        Must be a built-in type.
    """
