#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides containers for co-reference sentences.
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
    """A co-reference token.

    Attributes
    ----------
        word : str
            the token word.
        coref : Tuple[int, str]
            the co-reference ID and type. `None` if not a co-reference source or target.

            * **type**:
                * `'source'`: co-reference source.
                * `'target'`: co-reference target.
                * `'zero'`: null element co-reference target.

        idx : int
            the node index in parsed tree.

    Note
    ----
        This class is an subclass of :class:`tuple`. To change the attribute, please create a new instance instead.

    .. admonition:: Data Structure Examples

        Text format
            Not implemented

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                {
                    'word': '中文字',   # token word
                    'coref': 'LANGUAGE', # coref-tag
                    'idx': (0, 3),     # starting / ending index.
                }

        List format
            Used for :meth:`from_list` and :meth:`to_list`.

            .. code-block:: python

                [
                    '中文字'     # token word
                    'LANGUAGE', # coref-tag
                    (0, 3),     # starting / ending index.
                ]
    """

    to_text = NotImplemented
    from_text = NotImplemented

################################################################################################################################

class CorefSentence(_BaseSentence):
    """A list of co-reference sentence.

    .. admonition:: Data Structure Examples

        Text format
            Not implemented

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                [
                    { 'word': '美國', 'coref': 'GPE', 'idx': (0, 2), },   # name-entity 1
                    { 'word': '參議院', 'coref': 'ORG', 'idx': (3, 5), }, # name-entity 2
                ]

        List format
            Used for :meth:`from_list` and :meth:`to_list`.

            .. code-block:: python

                [
                    [ '美國', 'GPE', (0, 2), ],   # name-entity 1
                    [ '參議院', 'ORG', (3, 5), ], # name-entity 2
                ]
    """

    item_class = CorefToken

    to_text = NotImplemented
    from_text = NotImplemented

################################################################################################################################

class CorefParagraph(_BaseList):
    """A list of co-reference sentence.

    .. admonition:: Data Structure Examples

        Text format
            Not implemented

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                [
                    [ # Sentence 1
                        { 'word': '中文字', 'coref': 'LANGUAGE', 'idx': (0, 3), },
                    ],
                    [ # Sentence 2
                        { 'word': '美國', 'coref': 'GPE', 'idx': (0, 2), },
                        { 'word': '參議院', 'coref': 'ORG', 'idx': (3, 5), },
                    ],
                ]

        List format
            Used for :meth:`from_list` and :meth:`to_list`.

            .. code-block:: python

                [
                    [ # Sentence 1
                        [ '中文字', 'LANGUAGE', (0, 3), ],
                    ],
                    [ # Sentence 2
                        [ '美國', 'GPE', (0, 2), ],
                        [ '參議院', 'ORG', (3, 5), ],
                    ],
                ]
    """

    item_class = CorefSentence

    to_text = NotImplemented
    from_text = NotImplemented
