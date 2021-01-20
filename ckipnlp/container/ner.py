#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides containers for NER sentences.
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

class _NerToken(_NamedTuple):
    word: str
    ner: str
    idx: _Tuple[int, int]

class NerToken(_BaseTuple, _NerToken):
    """A named-entity recognition token.

    Attributes
    ----------
        word : str
            the token word.
        ner : str
            the NER-tag.
        idx : Tuple[int, int]
            the starting / ending index.

    Note
    ----
        This class is an subclass of :class:`tuple`. To change the attribute, please create a new instance instead.

    .. admonition:: Data Structure Examples

        Text format
            Not implemented

        List format
            Used for :meth:`from_list` and :meth:`to_list`.

            .. code-block:: python

                [
                    '中文字'     # token word
                    'LANGUAGE', # NER-tag
                    (0, 3),     # starting / ending index.
                ]

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                {
                    'word': '中文字',   # token word
                    'ner': 'LANGUAGE', # NER-tag
                    'idx': (0, 3),     # starting / ending index.
                }

        CkipTagger format
            Used for :meth:`from_tagger` and :meth:`to_tagger`.

            .. code-block:: python

                (
                    0,          # starting index
                    3,          # ending index
                    'LANGUAGE', # NER-tag
                    '中文字',    # token word
                )
    """

    def __new__(cls, word, ner, idx, **kwargs):  # pylint: disable=signature-differs
        return super().__new__(cls, word, ner, tuple(idx), **kwargs)

    to_text = NotImplemented
    from_text = NotImplemented

    ########################################################################################################################

    @classmethod
    def from_tagger(cls, data):
        """Construct an instance from CkipTagger format."""
        idx0, idx1, ner, word = data
        return cls(word=word, ner=ner, idx=(idx0, idx1,))  # pylint: disable=no-value-for-parameter

    def to_tagger(self):
        """Transform to CkipTagger format."""
        return (*self.idx, self.ner, self.word)

################################################################################################################################

class NerSentence(_BaseSentence):
    """A named-entity recognition sentence.

    .. admonition:: Data Structure Examples

        Text format
            Not implemented

        List format
            Used for :meth:`from_list` and :meth:`to_list`.

            .. code-block:: python

                [
                    [ '美國', 'GPE', (0, 2), ],   # name-entity 1
                    [ '參議院', 'ORG', (3, 5), ], # name-entity 2
                ]

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                [
                    { 'word': '美國', 'ner': 'GPE', 'idx': (0, 2), },   # name-entity 1
                    { 'word': '參議院', 'ner': 'ORG', 'idx': (3, 5), }, # name-entity 2
                ]

        CkipTagger format
            Used for :meth:`from_tagger` and :meth:`to_tagger`.

            .. code-block:: python

                [
                    ( 0, 2, 'GPE', '美國', ),   # name-entity 1
                    ( 3, 5, 'ORG', '參議院', ), # name-entity 2
                ]
    """

    item_class = NerToken

    to_text = NotImplemented
    from_text = NotImplemented

    ########################################################################################################################

    @classmethod
    def from_tagger(cls, data):
        """Construct an instance from CkipTagger format."""
        return cls(map(cls.item_class.from_tagger, data))

    def to_tagger(self):
        """Transform to CkipTagger format."""
        return list(item.to_tagger() for item in self)

################################################################################################################################

class NerParagraph(_BaseList):
    """A list of named-entity recognition sentence.

    .. admonition:: Data Structure Examples

        Text format
            Not implemented

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

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                [
                    [ # Sentence 1
                        { 'word': '中文字', 'ner': 'LANGUAGE', 'idx': (0, 3), },
                    ],
                    [ # Sentence 2
                        { 'word': '美國', 'ner': 'GPE', 'idx': (0, 2), },
                        { 'word': '參議院', 'ner': 'ORG', 'idx': (3, 5), },
                    ],
                ]

        CkipTagger format
            Used for :meth:`from_tagger` and :meth:`to_tagger`.

            .. code-block:: python

                [
                    [ # Sentence 1
                        ( 0, 3, 'LANGUAGE', '中文字', ),
                    ],
                    [ # Sentence 2
                        ( 0, 2, 'GPE', '美國', ),
                        ( 3, 5, 'ORG', '參議院', ),
                    ],
                ]
    """

    item_class = NerSentence

    to_text = NotImplemented
    from_text = NotImplemented

    ########################################################################################################################

    @classmethod
    def from_tagger(cls, data):
        """Construct an instance from CkipTagger format."""
        return cls(map(cls.item_class.from_tagger, data))

    def to_tagger(self):
        """Transform to CkipTagger format."""
        return list(item.to_tagger() for item in self)
