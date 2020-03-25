#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides base containers.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import json as _json

from collections import (
    UserList as _UserList,
)

################################################################################################################################

class Base:
    """The base CKIPNLP container."""

    def __str__(self):
        return self.to_text()

    ########################################################################################################################

    @classmethod
    def from_text(cls, data):
        """Construct an instance from text format."""
        raise NotImplementedError

    def to_text(self):
        """Transform to plain text."""
        raise NotImplementedError

    ########################################################################################################################

    @classmethod
    def from_dict(cls, data):
        """Construct an instance a from python built-in containers."""
        raise NotImplementedError

    def to_dict(self):
        """Transform to python built-in containers."""
        raise NotImplementedError

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

        Return
        ------
            str
        """
        return _json.dumps(self.to_dict(), **kwargs)

################################################################################################################################

class BaseList(Base, _UserList):
    """The base CKIPNLP list."""

    item_class = NotImplemented

    ########################################################################################################################

    @classmethod
    def _item_from_text(cls, data):
        return cls.item_class.from_text(data)  # pylint: disable=no-member

    @classmethod
    def _item_to_text(cls, item):
        return cls.item_class.to_text(item)  # pylint: disable=no-member

    @classmethod
    def _item_from_dict(cls, data):
        return cls.item_class.from_dict(data)  # pylint: disable=no-member

    @classmethod
    def _item_to_dict(cls, item):
        return cls.item_class.to_dict(item)  # pylint: disable=no-member

    ########################################################################################################################

    @classmethod
    def from_text(cls, data):
        """Construct an instance from text format.

        Parameters
        ----------
            data : Sequence[str]
                list of texts as ``item_class.from_text`` input.
        """
        return cls(map(cls._item_from_text, data))

    def to_text(self):
        """Transform to plain text.

        Return
        ------
            List[str]
        """
        return list(map(self._item_to_text, self))

    ########################################################################################################################

    @classmethod
    def from_dict(cls, data):
        """Construct an instance a from python built-in containers.

        Parameters
        ----------
            data : Sequence[Sequence[Container]]
                list of objects as ``item_class.from_dict`` input.
        """
        return cls(map(cls._item_from_dict, data))

    def to_dict(self):
        """Transform to python built-in containers.

        Return
        ------
            List[List[Container]]
        """
        return list(map(self._item_to_dict, self))

################################################################################################################################

class BaseSentence(BaseList):
    """The base CKIPNLP sentence."""

    @classmethod
    def from_text(cls, data):
        """Construct an instance from text format.

        Parameters
        ----------
            data : str
                words segmented by ``'\\u3000'``.
        """
        return cls(map(cls._item_from_text, data.split('\u3000')))

    def to_text(self):
        """Transform to plain text.

        Return
        ------
            str
        """
        return '\u3000'.join(map(self._item_to_text, self))
