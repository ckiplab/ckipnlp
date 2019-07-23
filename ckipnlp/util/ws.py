#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2018-2019'

import collections as _collections

class WsWord(_collections.namedtuple('_WsWord', ('word', 'pos',))):
    """A word-segmented word.

    Fields:
        * **word** (*str*): the word.
        * **pos** (*str*): the post-tag.
    """

    @classmethod
    def from_text(cls, text):
        """Create :class:`WsWord` object from :class:`ckipnlp.ws.CkipWs` output."""
        return cls(*text.strip(')').rsplit('(', 1))

    def __str__(self):
        return '{}({})'.format(self.word, self.pos)

class WsSentence(_collections.UserList): # pylint: disable=too-many-ancestors
    """A word-segmented sentence.

    Items:
        :class:`WsWord`: the words.
    """

    @classmethod
    def from_text(cls, text):
        """Create :class:`WsSentence` object from :class:`ckipnlp.ws.CkipWs` output."""
        return cls(map(WsWord.from_text, text.split('\u3000')))

    def __str__(self):
        return '\u3000'.join(map(str, self))
