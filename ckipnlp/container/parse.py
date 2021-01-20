#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides containers for parsed sentences.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

from typing import (
    NamedTuple as _NamedTuple,
)

from .base import (
    BaseTuple as _BaseTuple,
    BaseList as _BaseList,
)

from .util.parse_tree import (
    ParseTree as _ParseTree,
)

################################################################################################################################

class _ParseClause(_NamedTuple):
    clause: str = None
    delim: str = ''

class ParseClause(_BaseTuple, _ParseClause):
    """A parse clause.

    Attributes
    ----------
        clause : str
            the parse clause.
        delim : str
            the punctuations after this clause.

    Note
    ----
        This class is an subclass of :class:`tuple`. To change the attribute, please create a new instance instead.

    .. admonition:: Data Structure Examples

        Text format
            Used for :meth:`to_text`.

            .. code-block:: python

                'S(Head:Nab:中文字|particle:Td:耶)' # delim are ignored

        List format
            Used for :meth:`from_list`, and :meth:`to_list`.

            .. code-block:: python

                [
                    'S(Head:Nab:中文字|particle:Td:耶)', # parse clause
                    '，',                               # punctuations
                ]

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                {
                    'clause': 'S(Head:Nab:中文字|particle:Td:耶)', # parse clause
                    'delim': '，',                                # punctuations
                }
    """

    from_text = NotImplemented

    def to_text(self):
        return self.clause

    def to_tree(self):
        """Transform to tree format.

        Returns
        -------
            :class:`~.util.parse_tree.ParseTree`
                the tree format of this clause. (`None` if **clause** is `None`)

        .. seealso::
            :meth:`ParseTree.from_text() <.util.parse_tree.ParseTree.from_text>`.

        """
        return _ParseTree.from_text(self.clause) if self.clause else None

################################################################################################################################

class ParseSentence(_BaseList):
    """A parse sentence.

    .. admonition:: Data Structure Examples

        Text format
            Used for :meth:`to_text`.

            .. code-block:: python

                [ # delim are ignored
                    'S(Head:Nab:中文字|particle:Td:耶)',                    # Clause 1
                    '%(particle:I:啊|manner:Dh:哈|manner:Dh:哈|time:Dh:哈), # Clause 2
                ]

        List format
            Used for :meth:`from_list`, and :meth:`to_list`.

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

    from_text = NotImplemented

    item_class = ParseClause

class ParseParagraph(_BaseList):
    """A list of parse sentence.

    .. admonition:: Data Structure Examples

        Text format
            Used for :meth:`to_text`.

            .. code-block:: python

                [ # delim are ignored
                    [ # Sentence 1
                        'S(Head:Nab:中文字|particle:Td:耶)',
                        '%(particle:I:啊|manner:Dh:哈|manner:Dh:哈|time:Dh:哈),
                    ],
                    [ # Sentence 2
                        None,
                        'VP(Head:VH11:完蛋|particle:Ta:了),
                        'S(agent:NP(apposition:Nba:畢卡索|Head:Nhaa:他)|Head:VE2:想)',
                    ],
                ]

        List format
            Used for :meth:`from_list`, and :meth:`to_list`.

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
                            'delim': '！」',
                        },
                        {
                            'clause': 'S(agent:NP(apposition:Nba:畢卡索|Head:Nhaa:他)|Head:VE2:想)',
                            'delim': '',
                        },
                    ],
                ]
    """

    from_text = NotImplemented

    item_class = ParseSentence
