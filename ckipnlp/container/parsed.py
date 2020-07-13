#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides containers for parsed sentences.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from typing import (
    NamedTuple as _NamedTuple,
)

from .base import (
    BaseTuple as _BaseTuple,
    BaseList as _BaseList,
)

################################################################################################################################

class _ParsedClause(_NamedTuple):
    clause: str
    delim: str

class ParsedClause(_BaseTuple, _ParsedClause):
    """A parsed clause.

    Attributes
    ----------
        clause : str
            the parsed clause.
        delim : str
            the punctuations after this clause.

    Note
    ----
        This class is an subclass of :class:`tuple`. To change the attribute, please create a new instance instead.

    .. admonition:: Data Structure Examples

        Text/List format
            Used for :meth:`from_text`, :meth:`to_text`, :meth:`from_list`, and :meth:`to_list`.

            .. code-block:: python

                [
                    'S(Head:Nab:中文字|particle:Td:耶)', # parsed clause
                    '，',                               # punctuations
                ]

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                {
                    'clause': 'S(Head:Nab:中文字|particle:Td:耶)', # parsed clause
                    'delim': '，',                                # punctuations
                }
    """

    @classmethod
    def from_text(cls, data):
        return cls.from_list(data)

    def to_text(self):
        return self.to_list()

################################################################################################################################

class ParsedSentence(_BaseList):
    """A parsed sentence.

    .. admonition:: Data Structure Examples

        Text/List format
            Used for :meth:`from_text`, :meth:`to_text`, :meth:`from_list`, and :meth:`to_list`.

            .. code-block:: python

                [
                    [ # Clause 1
                        'S(Head:Nab:中文字|particle:Td:耶)',
                        '，',
                    ],
                    [ # Clause 2
                        '%(particle:I:啊|manner:Dh:哈|manner:Dh:哈|time:Dh:哈),
                        '。',
                    ],
                ]

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                [
                    { # Clause 1
                        'clause': 'S(Head:Nab:中文字|particle:Td:耶)',
                        'delim': '，',
                    },
                    { # Clause 2
                        'clause': '%(particle:I:啊|manner:Dh:哈|manner:Dh:哈|time:Dh:哈),
                        'delim': '。',
                    },
                ]

    """

    item_class = ParsedClause

class ParsedParagraph(_BaseList):
    """A list of parsed sentence.

    .. admonition:: Data Structure Examples

        Text/List format
            Used for :meth:`from_text`, :meth:`to_text`, :meth:`from_list`, and :meth:`to_list`.

            .. code-block:: python

                [
                    [ # Sentence 1
                        [
                            'S(Head:Nab:中文字|particle:Td:耶)',
                            '，',
                        ],
                        [
                            '%(particle:I:啊|manner:Dh:哈|manner:Dh:哈|time:Dh:哈),
                            '。',
                        ],
                    ],
                    [ # Sentence 2
                        [
                            None,
                            '「',
                        ],
                        [
                            'VP(Head:VH11:完蛋|particle:Ta:了),
                            '！」',
                        ],
                        [
                            'S(agent:NP(apposition:Nba:畢卡索|Head:Nhaa:他)|Head:VE2:想)',
                            '',
                        ],
                    ],
                ]

        Dict format
            Used for :meth:`from_dict`, and :meth:`to_dict`.

            .. code-block:: python

                [
                    [ # Sentence 1
                        {
                            'clause': 'S(Head:Nab:中文字|particle:Td:耶)',
                            'delim': '，',
                        },
                        {
                            'clause': '%(particle:I:啊|manner:Dh:哈|manner:Dh:哈|time:Dh:哈),
                            'delim': '。',
                        },
                    ],
                    [ # Sentence 2
                        {
                            'clause': None,
                            'delim': '「',
                        },
                        {
                            'clause': 'VP(Head:VH11:完蛋|particle:Ta:了),
                            'delim': '！」，',
                        },
                        {
                            'clause': 'S(agent:NP(apposition:Nba:畢卡索|Head:Nhaa:他)|Head:VE2:想)',
                            'delim': '',
                        },
                    ],
                ]
    """

    item_class = ParsedSentence
