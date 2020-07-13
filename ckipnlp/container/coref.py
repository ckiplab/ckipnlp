#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides containers for coreference sentences.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from typing import (
    NamedTuple as _NamedTuple,
    Tuple as _Tuple,
)

from .base import (
    BaseTuple as _BaseTuple,
    BaseList as _BaseList,
    BaseSentence as _BaseSentence,
)

################################################################################################################################

class _CorefToken(_NamedTuple):
    word: str
    coref: _Tuple[int, str,]
    idx: int

class CorefToken(_BaseTuple, _CorefToken):
    """A coreference token.

    Attributes
    ----------
        word : str
            the token word.
        coref : Tuple[int, str]
            the coreference ID and type. `None` if not a coreference source or target.

            * **type**:
                * `'source'`: coreference source.
                * `'target'`: coreference target.
                * `'zero'`: null element coreference target.

        idx : Tuple[int, int]
            the node indexes (clause index, token index) in parsed tree.
            **idx[1]** = `None` if this node is a null element or the punctuations.

    Note
    ----
        This class is an subclass of :class:`tuple`. To change the attribute, please create a new instance instead.

    .. admonition:: Data Structure Examples

        Text format
            Used for :meth:`to_text`.

            .. code-block:: python

                '畢卡索_0'

        List format
            Used for :meth:`from_list` and :meth:`to_list`.

            .. code-block:: python

                [
                    '畢卡索',       # token word
                    (0, 'source'), # coref ID and type
                    (2, 0),        # node index
                ]

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                {
                    'word': '畢卡索',        # token word
                    'coref': (0, 'source'), # coref ID and type
                    'idx': (2, 0),          # node index
                }
    """

    from_text = NotImplemented

    def to_text(self):
        return f'{self.word}_{self.coref[0]}' if self.coref else self.word

################################################################################################################################

class CorefSentence(_BaseSentence):
    """A list of coreference sentence.

    .. admonition:: Data Structure Examples

        Text format
            Used for :meth:`to_text`.

            .. code-block:: python

                # Token segmented by \\u3000 (full-width space)
                '「\u3000完蛋\u3000了\u3000！」\u3000，\u3000畢卡索_0\u3000他_0\u3000想'

        List format
            Used for :meth:`from_list` and :meth:`to_list`.

            .. code-block:: python

                [
                    [ '「', None, (0, 0,) ],
                    [ '完蛋', None, (1, 0,) ],
                    [ '了', None, (1, 1,) ],
                    [ '！」', None, (1, 2,) ],
                    [ '畢卡索', (0, 'source'), (2, 0,), ],
                    [ '他', (0, 'target'), (2, 1,), ],
                    [ '想', None, (2, 2,), ],
                ]

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                [
                    { 'word': '「', 'coref': None, 'idx': (0, 0,) ],
                    { 'word': '完蛋', 'coref': None, 'idx': (1, 0,) ],
                    { 'word': '了', 'coref': None, 'idx': (1, 1,) ],
                    { 'word': '！」', 'coref': None, 'idx': (1, 2,) ],
                    { 'word': '畢卡索', 'coref': (0, 'source'), 'idx': (2, 0,), ],
                    { 'word': '他', 'coref': (0, 'target'), 'idx': (2, 1,), ],
                    { 'word': '想', 'coref': None, 'idx': (2, 2,), ],
                ]
    """

    item_class = CorefToken

    from_text = NotImplemented

    def to_text(self):
        return '\u3000'.join(map(self._item_to_text, self))

################################################################################################################################

class CorefParagraph(_BaseList):
    """A list of coreference sentence.

    .. admonition:: Data Structure Examples

        Text format
            Used for :meth:`to_text`.

            .. code-block:: python

                [
                    '「\u3000完蛋\u3000了\u3000！」\u3000，\u3000畢卡索_0\u3000他_0\u3000想', # Sentence 1
                    '然後\u3000None_0\u3000就\u3000跑\u3000了', # Sentence 1
                ]

        List format
            Used for :meth:`from_list` and :meth:`to_list`.

            .. code-block:: python

                [
                    [ # Sentence 1
                        [ '「', None, (0, 0,) ],
                        [ '完蛋', None, (1, 0,) ],
                        [ '了', None, (1, 1,) ],
                        [ '！」', None, (1, 2,) ],
                        [ '畢卡索', (0, 'source'), (2, 0,), ],
                        [ '他', (0, 'target'), (2, 1,), ],
                        [ '想', None, (2, 2,), ],
                    ],
                    [ # Sentence 2
                        [ '然後', None, (0, 0,) ],
                        [ None, (0, 'zero'), (0, 1,) ],
                        [ '就', None, (0, 2,) ],
                        [ '跑', None, (0, 3,) ],
                        [ '了', None, (0, 4,) ],
                    ],
                ]

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                [
                    [ # Sentence 1
                        { 'word': '「', 'coref': None, 'idx': (0, 0,) ],
                        { 'word': '完蛋', 'coref': None, 'idx': (1, 0,) ],
                        { 'word': '了', 'coref': None, 'idx': (1, 1,) ],
                        { 'word': '！」', 'coref': None, 'idx': (1, 2,) ],
                        { 'word': '畢卡索', 'coref': (0, 'source'), 'idx': (2, 0,), ],
                        { 'word': '他', 'coref': (0, 'target'), 'idx': (2, 1,), ],
                        { 'word': '想', 'coref': None, 'idx': (2, 2,), ],
                    ],
                    [ # Sentence 2
                        { 'word': '然後', 'coref': None, 'idx': (0, 0,) ],
                        { 'word': None, 'coref': (0, 'zero'), 'idx': (1, 0,) ],
                        { 'word': '就', 'coref': None, 'idx': (2, 0,) ],
                        { 'word': '跑', 'coref': None, 'idx': (3, 0,) ],
                        { 'word': '了', 'coref': None, 'idx': (4, 0,) ],
                    ],
                ]
    """

    item_class = CorefSentence

    from_text = NotImplemented
