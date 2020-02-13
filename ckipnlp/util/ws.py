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

class WsWord(NamedTuple):
    """A word-segmented word."""

    word: str #: *str* – the word.
    pos: str  #: *str* – the post-tag.

    @classmethod
    def from_text(cls, text):
        """Create a :class:`WsWord` object from :class:`ckipnlp.ws.CkipWs` output.

        Parameters
        ----------
            text : str
                A word from :class:`ckipnlp.ws.CkipWs` output.
        """
        return cls(*text.strip(')').rsplit('(', 1))

    def __str__(self):
        return self.to_text()

    def to_text(self):
        """Transform to plain text."""
        return '{}({})'.format(self.word, self.pos)

    def to_dict(self):
        """Transform to python dict/list."""
        return self._asdict() # pylint: disable=no-member

    def to_json(self, **kwargs):
        """Transform to JSON format."""
        return _json.dumps(self.to_dict(), **kwargs)

class WsSentence(_collections.UserList): # pylint: disable=too-many-ancestors
    """A word-segmented sentence."""

    item_class = WsWord

    @classmethod
    def from_text(cls, text):
        """Create :class:`WsSentence` object from :class:`ckipnlp.ws.CkipWs` output.

        Parameters
        ----------
            text : str
                A sentence from :class:`ckipnlp.ws.CkipWs` output.
        """
        return cls(map(cls.item_class.from_text, text.split('\u3000')))

    def __str__(self):
        return self.to_text()

    def to_text(self):
        """Transform to plain text."""
        return '\u3000'.join(map(self.item_class.to_text, self))

    def to_dict(self):
        """Transform to python dict/list."""
        return [word.to_dict() for word in self]

    def to_json(self, **kwargs):
        """Transform to JSON format."""
        return _json.dumps(self.to_dict(), **kwargs)


class WsSentenceList(_collections.UserList): # pylint: disable=too-many-ancestors
    """A list of word-segmented sentence."""

    item_class = WsSentence

    @classmethod
    def from_text(cls, text_list):
        """Create :class:`WsSentenceList` object from :class:`ckipnlp.ws.CkipWs` output.

        Parameters
        ----------
            text_list : List[str]
                A list of sentence from :class:`ckipnlp.ws.CkipWs` output.
        """
        return cls(map(cls.item_class.from_text, text_list))

    def __str__(self):
        return self.to_text()

    def to_text(self):
        """Transform to plain text."""
        return '\n'.join(map(self.item_class.to_text, self))

    def to_dict(self):
        """Transform to python dict/list."""
        return [sentence.to_dict() for sentence in self]

    def to_json(self, **kwargs):
        """Transform to JSON format."""
        return _json.dumps(self.to_dict(), **kwargs)
