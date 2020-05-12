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

        idx : int
            the node index in parsed tree.

    Note
    ----
        This class is an subclass of :class:`tuple`. To change the attribute, please create a new instance instead.

    .. admonition:: Data Structure Examples

        Text format
            Used for :meth:`to_text`.

            .. code-block:: python

                '畢卡索_0'

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                {
                    'word': '畢卡索',        # token word
                    'coref': (0, 'source'), # coref ID and type
                    'idx': 2,               # node index
                }

        List format
            Used for :meth:`from_list` and :meth:`to_list`.

            .. code-block:: python

                [
                    '畢卡索',       # token word
                    (0, 'source'), # coref ID and type
                    2,             # node index
                ]
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

                '畢卡索_0\u3000他_0\u3000想' # Token segmented by \\u3000 (full-width space)

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                [
                    { 'word': '畢卡索', 'coref': (0, 'source'), 'idx': 2, }, # coref-token 1
                    { 'word': '他', 'coref': (0, 'target'), 'idx': 3, },    # coref-token 2
                    { 'word': '想', 'coref': None, 'idx': 4, },             # coref-token 3
                ]

        List format
            Used for :meth:`from_list` and :meth:`to_list`.

            .. code-block:: python

                [
                    [ '畢卡索', (0, 'source'), 2, ], # coref-token 1
                    [ '他', (0, 'target'), 3, ],    # coref-token 2
                    [ '想', None, 4, ],             # coref-token 3
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
                    '畢卡索_0\u3000他_0\u3000想', # Sentence 1
                    'None_0\u3000完蛋\u3000了',  # Sentence 2
                ]

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                [
                    [ # Sentence 1
                        { 'word': '畢卡索', 'coref': (0, 'source'), 'idx': 2, },
                        { 'word': '他', 'coref': (0, 'target'), 'idx': 3, },
                        { 'word': '想', 'coref': None, 'idx': 4, },
                    ],
                    [ # Sentence 2
                        { 'word': None, 'coref': (0, 'zero'), None, },
                        { 'word': '完蛋', 'coref': None, 'idx': 1, },
                        { 'word': '了', 'coref': None, 'idx': 2, },
                    ],
                ]

        List format
            Used for :meth:`from_list` and :meth:`to_list`.

            .. code-block:: python

                [
                    [ # Sentence 1
                        [ '畢卡索', (0, 'source'), 2, ],
                        [ '他', (0, 'target'), 3, ],
                        [ '想', None, 4, ],
                    ],
                    [ # Sentence 2
                        [ None, (0, 'zero'), None, ],
                        [ '完蛋', None, 1, ],
                        [ '了', None, 2, ],
                    ],
                ]
    """

    item_class = CorefSentence

    from_text = NotImplemented
