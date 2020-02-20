#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import collections as _collections
import json as _json

from typing import (
    NamedTuple,
)

################################################################################################################################

class WsWord(NamedTuple):
    """A word-segmented word."""

    word: str = None #: *str* – the word.
    pos: str = None  #: *str* – the post-tag.

    def __str__(self):
        return self.to_text()

    @classmethod
    def from_text(cls, data):
        """Construct an instance from :class:`ckipnlp.ws.CkipWs` output.

        Parameters
        ----------
            data : str
                text such as ``'中文字(Na)'``.

        Notes
        -----
            - ``'中文字(Na)'`` -> word = ``'中文字'``, pos = ``'Na'``
            - ``'中文字'``     -> word = ``'中文字'``, pos = ``None``
        """
        return cls(*data.strip(')').rsplit('(', 1))

    def to_text(self):
        """Transform to plain text.

        Return
        ------
            str
        """
        return '{}({})'.format(self.word, self.pos)

    @classmethod
    def from_dict(cls, data):
        """Construct an instance from python built-in containers.

        Parameters
        ----------
            data : dict
                dictionary such as ``{ 'word': '中文字', 'pos': 'Na' }``
        """
        return cls(**data)

    def to_dict(self):
        """Transform to python built-in containers.

        Return
        ------
            dict
        """
        return self._asdict() # pylint: disable=no-member

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

class WsSentence(_collections.UserList): # pylint: disable=too-many-ancestors
    """A word-segmented sentence."""

    item_class = WsWord

    def __str__(self):
        return self.to_text()

    @classmethod
    def from_text(cls, data):
        """Construct an instance from :class:`ckipnlp.ws.CkipWs` output.

        Parameters
        ----------
            data : str
                text such as ``'中文字(Na)\\u3000喔(T)'``.
        """
        return cls(map(cls.item_class.from_text, data.split('\u3000')))

    def to_text(self):
        """Transform to plain text.

        Return
        ------
            str
        """
        return '\u3000'.join(map(self.item_class.to_text, self))

    @classmethod
    def from_dict(cls, data):
        """Construct an instance a from python built-in containers.

        Parameters
        ----------
            data : Sequence[dict]
                list of objects as :meth:`WsWord.from_dict` input.
        """
        return cls(map(cls.item_class.from_dict, data))

    def to_dict(self):
        """Transform to python built-in containers.

        Return
        ------
            List[dict]
        """
        return [word.to_dict() for word in self]

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

class WsSentenceList(_collections.UserList): # pylint: disable=too-many-ancestors
    """A list of word-segmented sentence."""

    item_class = WsSentence

    def __str__(self):
        return self.to_text()

    @classmethod
    def from_text(cls, data):
        """Construct an instance from :class:`ckipnlp.ws.CkipWs` output.

        Parameters
        ----------
            data : Sequence[str]
                list of texts as :meth:`WsSentence.from_text` input.
        """
        return cls(map(cls.item_class.from_text, data))

    def to_text(self):
        """Transform to plain text.

        Return
        ------
            List[str]
        """
        return list(map(self.item_class.to_text, self))

    @classmethod
    def from_dict(cls, data):
        """Construct an instance a from python built-in containers.

        Parameters
        ----------
            data : Sequence[Sequence[dict]]
                list of objects as :meth:`WsSentence.from_dict` input.
        """
        return cls(map(cls.item_class.from_dict, data))

    def to_dict(self):
        """Transform to python built-in containers.

        Return
        ------
            List[List[dict]]
        """
        return [sentence.to_dict() for sentence in self]

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
