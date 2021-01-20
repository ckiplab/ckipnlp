#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides containers for coreference sentences.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

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
            the node indexes (clause index, token index) in parse tree.
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
                    (2, 2),        # node index
                ]

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                {
                    'word': '畢卡索',        # token word
                    'coref': (0, 'source'), # coref ID and type
                    'idx': (2, 2),          # node index
                }
    """

    def __new__(cls, word, coref, idx, **kwargs):  # pylint: disable=signature-differs
        return super().__new__(cls, word, tuple(coref) if coref else None, tuple(idx), **kwargs)

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
                    [ '「', None, (0, None,), ],
                    [ '完蛋', None, (1, 0,), ],
                    [ '了', None, (1, 1,), ],
                    [ '！」', None, (1, None,), ],
                    [ '畢卡索', (0, 'source'), (2, 2,), ],
                    [ '他', (0, 'target'), (2, 3,), ],
                    [ '想', None, (2, 4,), ],
                ]

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                [
                    { 'word': '「', 'coref': None, 'idx': (0, None,), },
                    { 'word': '完蛋', 'coref': None, 'idx': (1, 0,), },
                    { 'word': '了', 'coref': None, 'idx': (1, 1,), },
                    { 'word': '！」', 'coref': None, 'idx': (1, None,), },
                    { 'word': '畢卡索', 'coref': (0, 'source'), 'idx': (2, 2,), },
                    { 'word': '他', 'coref': (0, 'target'), 'idx': (2, 3,), },
                    { 'word': '想', 'coref': None, 'idx': (2, 4,), },
                ]
    """

    item_class = CorefToken

    from_text = NotImplemented

################################################################################################################################

class CorefParagraph(_BaseList):
    """A list of coreference sentence.

    .. admonition:: Data Structure Examples

        Text format
            Used for :meth:`to_text`.

            .. code-block:: python

                [
                    '「\u3000完蛋\u3000了\u3000！」\u3000，\u3000畢卡索_0\u3000他_0\u3000想', # Sentence 1
                    '但是\u3000None_0\u3000也\u3000沒有\u3000辦法', # Sentence 1
                ]

        List format
            Used for :meth:`from_list` and :meth:`to_list`.

            .. code-block:: python

                [
                    [ # Sentence 1
                        [ '「', None, (0, None,), ],
                        [ '完蛋', None, (1, 0,), ],
                        [ '了', None, (1, 1,), ],
                        [ '！」', None, (1, None,), ],
                        [ '畢卡索', (0, 'source'), (2, 2,), ],
                        [ '他', (0, 'target'), (2, 3,), ],
                        [ '想', None, (2, 4,), ],
                    ],
                    [ # Sentence 2
                        [ '但是', None, (0, 1,), ],
                        [ None, (0, 'zero'), (0, None,), ],
                        [ '也', None, (0, 2,), ],
                        [ '沒有', None, (0, 3,), ],
                        [ '辦法', None, (0, 5,), ],
                    ],
                ]

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                [
                    [ # Sentence 1
                        { 'word': '「', 'coref': None, 'idx': (0, None,), },
                        { 'word': '完蛋', 'coref': None, 'idx': (1, 0,), },
                        { 'word': '了', 'coref': None, 'idx': (1, 1,), },
                        { 'word': '！」', 'coref': None, 'idx': (1, None,), },
                        { 'word': '畢卡索', 'coref': (0, 'source'), 'idx': (2, 2,), },
                        { 'word': '他', 'coref': (0, 'target'), 'idx': (2, 3,), },
                        { 'word': '想', 'coref': None, 'idx': (2, 4,), },
                    ],
                    [ # Sentence 2
                        { 'word': '但是', 'coref': None, 'idx': (0, 1,), },
                        { 'word': None, 'coref': (0, 'zero'), 'idx': (0, None,), },
                        { 'word': '也', 'coref': None, 'idx': (0, 2,), },
                        { 'word': '沒有', 'coref': None, 'idx': (0, 3,), },
                        { 'word': '辦法', 'coref': None, 'idx': (0, 5,), },
                    ],
                ]
    """

    item_class = CorefSentence

    from_text = NotImplemented
