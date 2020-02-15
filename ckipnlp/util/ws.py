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

    word: str #: *str* – the word.
    pos: str  #: *str* – the post-tag.

    def __str__(self):
        return self.to_text()

    @classmethod
    def from_text(cls, text):
        """Construct from :class:`ckipnlp.ws.CkipWs` output.

        Parameters
        ----------
            text : str
                A word from :class:`ckipnlp.ws.CkipWs` output.

        Return
        ------
            WsWord
        """
        return cls(*text.strip(')').rsplit('(', 1))

    def to_text(self):
        """Transform to plain text.

        Return
        ------
            str

        Return
        ------
            WsWord
        """
        return '{}({})'.format(self.word, self.pos)

    @classmethod
    def from_dict(cls, data):
        """Construct from python built-in containers.

        Parameters
        ----------
            data : dict
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
        """Construct from JSON format.

        Parameters
        ----------
            data : str

        Return
        ------
            :class:`WsWord`
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
    def from_text(cls, text):
        """Construct from :class:`ckipnlp.ws.CkipWs` output.

        Parameters
        ----------
            text : str
                A sentence from :class:`ckipnlp.ws.CkipWs` output.

        Return
        ------
            :class:`WsSentence`
        """
        return cls(map(cls.item_class.from_text, text.split('\u3000')))

    def to_text(self):
        """Transform to plain text.

        Return
        ------
            str
        """
        return '\u3000'.join(map(self.item_class.to_text, self))

    @classmethod
    def from_dict(cls, data):
        """Construct a from python built-in containers.

        Parameters
        ----------
            data : List[dict]

        Return
        ------
            :class:`WsSentence`
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
        """Construct from JSON format.

        Parameters
        ----------
            data : str

        Return
        ------
            :class:`WsSentence`
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
    def from_text(cls, text_list):
        """Construct from :class:`ckipnlp.ws.CkipWs` output.

        Parameters
        ----------
            text_list : List[str]
                A list of sentence from :class:`ckipnlp.ws.CkipWs` output.

        Return
        ------
            :class:`WsSentenceList`
        """
        return cls(map(cls.item_class.from_text, text_list))

    def to_text(self):
        """Transform to plain text.

        Return
        ------
            List[str]
        """
        return list(map(self.item_class.to_text, self))

    @classmethod
    def from_dict(cls, data):
        """Construct a from python built-in containers.

        Parameters
        ----------
            data : List[List[dict]]

        Return
        ------
            :class:`WsSentenceList`
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
        """Construct from JSON format.

        Parameters
        ----------
            data : str

        Return
        ------
            :class:`WsSentenceList`
        """
        return cls.from_dict(_json.loads(data, **kwargs))

    def to_json(self, **kwargs):
        """Transform to JSON format.

        Return
        ------
            str
        """
        return _json.dumps(self.to_dict(), **kwargs)
