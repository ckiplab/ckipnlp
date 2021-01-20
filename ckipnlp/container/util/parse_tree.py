#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
This module provides tree containers for parsed sentences.
"""

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'


from collections import (
    deque as _deque,
)

from typing import (
    NamedTuple as _NamedTuple,
)

from treelib import (
    Tree as _Tree,
    Node as _Node,
)

from ckipnlp.data.conparse import (
    SUBJECT_ROLES as _SUBJECT_ROLES,
    NEUTRAL_ROLES as _NEUTRAL_ROLES,
)

from ..base import (
    Base as _Base,
    BaseTuple as _BaseTuple,
)

################################################################################################################################

class _ParseNodeData(_NamedTuple):
    role: str = None
    pos: str = None
    word: str = None

class ParseNodeData(_BaseTuple, _ParseNodeData):
    """A parse node.

    Attributes
    ----------
        role : str
            the semantic role.
        pos : str
            the POS-tag.
        word : str
            the text term.

    Note
    ----
        This class is an subclass of :class:`tuple`. To change the attribute, please create a new instance instead.

    .. admonition:: Data Structure Examples

        Text format
            Used for :meth:`from_text` and :meth:`to_text`.

            .. code-block:: python

                'Head:Na:中文字'  # role / POS-tag / text-term

        List format
            Not implemented.

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.

            .. code-block:: python

                {
                    'role': 'Head',   # role
                    'pos': 'Na',      # POS-tag
                    'word': '中文字',  # text term
                }
    """

    from_list = NotImplemented
    to_list = NotImplemented

    @classmethod
    def from_text(cls, data):
        """Construct an instance from text format.

        Parameters
        ----------
            data : str
                text such as ``'Head:Na:中文字'``.

        .. note::

            - ``'Head:Na:中文字'`` -> **role** = ``'Head'``, **pos** = ``'Na'``, **word** = ``'中文字'``
            - ``'Head:Na'``       -> **role** = ``'Head'``, **pos** = ``'Na'``, **word** = ``None``
            - ``'Na'``            -> **role** = ``None``,   **pos** = ``'Na'``, **word** = ``None``
        """
        if ':' in data:
            fields = data.split(':')
            return cls(*fields)
        return cls(pos=data)  # pylint: disable=no-value-for-parameter

    def to_text(self):
        return ':'.join(filter(None, self))

################################################################################################################################

class ParseNode(_Base, _Node):
    """A parse node for tree.

    Attributes
    ----------
        data : :class:`ParseNodeData`

    See Also
    --------
        treelib.tree.Node: Please refer `<https://treelib.readthedocs.io/>`__ for built-in usages.

    .. admonition:: Data Structure Examples

        Text format
            Not implemented.

        List format
            Not implemented.

        Dict format
            Used for :meth:`to_dict`.

            .. code-block:: python

                {
                    'role': 'Head',   # role
                    'pos': 'Na',      # POS-tag
                    'word': '中文字',  # text term
                }
    """

    data_class = ParseNodeData

    from_dict = NotImplemented

    from_text = NotImplemented
    to_text = NotImplemented
    from_list = NotImplemented
    to_list = NotImplemented

    def __repr__(self):
        return '{name}(tag={tag}, identifier={identifier})'.format(
            name=self.__class__.__name__,
            tag=self.tag,
            identifier=self.identifier,
        )

    def to_dict(self):
        return dict(id=self.identifier, data=self.data.to_dict())

################################################################################################################################

class _ParseRelation(_NamedTuple):
    head: ParseNode
    tail: ParseNode
    relation: ParseNode

class ParseRelation(_Base, _ParseRelation):
    """A parse relation.

    Attributes
    ----------
        head : :class:`ParseNode`
            the head node.
        tail : :class:`ParseNode`
            the tail node.
        relation : :class:`ParseNode`
            the relation node. (the semantic role of this node is the relation.)

    Notes
    -----
        The parent of the relation node is always the common ancestor of the head node and tail node.

    .. admonition:: Data Structure Examples

        Text format
            Not implemented.

        List format
            Not implemented.

        Dict format
            Used for :meth:`to_dict`.

            .. code-block:: python

                {
                    'tail': { 'role': 'Head', 'pos': 'Nab', 'word': '中文字' }, # head node
                    'tail': { 'role': 'particle', 'pos': 'Td', 'word': '耶' }, # tail node
                    'relation': 'particle',  # relation
                }
    """

    from_dict = NotImplemented

    from_text = NotImplemented
    to_text = NotImplemented
    from_list = NotImplemented
    to_list = NotImplemented

    def __repr__(self):
        ret = '{name}(head=({head}, {head_id}), tail=({tail}, {tail_id}), relation=({rel}, {rel_id}))' if self.head_first \
         else '{name}(tail=({tail}, {tail_id}), head=({head}, {head_id}), relation=({rel}, {rel_id}))'
        return ret.format(
            name=type(self).__name__,
            head=self.head.tag,
            head_id=self.head.identifier,
            tail=self.tail.tag,
            tail_id=self.tail.identifier,
            rel=self.relation.data.role,
            rel_id=self.relation.identifier,
        )

    @property
    def head_first(self):  # pylint: disable=missing-docstring
        return self.head.identifier <= self.tail.identifier

    def to_dict(self):
        return dict(head=self.head.to_dict(), tail=self.tail.to_dict(), relation=self.relation.data.role)

################################################################################################################################

class ParseTree(_Base, _Tree):
    """A parse tree.

    See Also
    --------
        treereelib.tree.Tree: Please refer `<https://treelib.readthedocs.io/>`__ for built-in usages.

    .. admonition:: Data Structure Examples

        Text format
            Used for :meth:`from_text` and :meth:`to_text`.

            .. code-block:: python

                'S(Head:Nab:中文字|particle:Td:耶)'

        List format
            Not implemented.

        Dict format
            Used for :meth:`from_dict` and :meth:`to_dict`.
            A dictionary such as ``{ 'id': 0, 'data': { ... }, 'children': [ ... ] }``,
            where ``'data'`` is a dictionary with the same format as :meth:`ParseNodeData.to_dict`,
            and ``'children'`` is a list of dictionaries of subtrees with the same format as this tree.

            .. code-block:: python

                {
                    'id': 0,
                    'data': {
                        'role': None,
                        'pos': 'S',
                        'word': None,
                    },
                    'children': [
                        {
                            'id': 1,
                            'data': {
                                'role': 'Head',
                                'pos': 'Nab',
                                'word': '中文字',
                            },
                            'children': [],
                        },
                        {
                            'id': 2,
                            'data': {
                                'role': 'particle',
                                'pos': 'Td',
                                'word': '耶',
                            },
                            'children': [],
                        },
                    ],
                }

        Penn Treebank format
            Used for :meth:`from_penn` and :meth:`to_penn`.

            .. code-block:: python

                [
                    'S',
                    [ 'Head:Nab', '中文字', ],
                    [ 'particle:Td', '耶', ],
                ]

    .. note::

        One may use :meth:`to_penn` together with `SvgLing <https://pypi.org/project/svgling/>`__ to generate SVG tree graphs.

    """

    node_class = ParseNode

    from_list = NotImplemented
    to_list = NotImplemented

    def __str__(self):
        return self.to_text()

    ########################################################################################################################

    @classmethod
    def from_text(cls, data):
        """Construct an instance from text format.

        Parameters
        ----------
            data : str
                A parse tree in text format (:class:`ParseClause.clause <.parse.ParseClause>`).

        .. seealso::
            :meth:`ParseClause.to_tree() <.parse.ParseClause.to_tree>`.
        """

        tree = cls()
        node_id = 0
        node_stack = [None]
        text = ''
        ending = True

        for char in data:
            if char == '(':
                node_data = cls.node_class.data_class.from_text(text)
                tree.create_node(tag=text, identifier=node_id, parent=node_stack[-1], data=node_data)

                node_stack.append(node_id)
                node_id += 1
                text = ''

            elif char == ')':
                if not ending:
                    node_data = cls.node_class.data_class.from_text(text)
                    tree.create_node(tag=text, identifier=node_id, parent=node_stack[-1], data=node_data)
                    node_id += 1

                node_stack.pop()
                text = ''
                ending = True

            elif char == '|':
                if not ending:
                    node_data = cls.node_class.data_class.from_text(text)
                    tree.create_node(tag=text, identifier=node_id, parent=node_stack[-1], data=node_data)
                    node_id += 1

                text = ''
                ending = True

            else:
                ending = False
                text += char

        return tree

    def to_text(self, node_id=None):
        """Transform to plain text.

        Parameters
        ----------
            node_id : int
                Output the plain text format for the subtree under **node_id**.

        Returns
        --------
            str
        """
        if node_id is None:
            node_id = self.root

        node = self[node_id]
        tree_text = node.data.to_text()

        children_text = '|'.join((self.to_text(child.identifier) for child in self.children(node_id)))
        if children_text:
            tree_text = '{}({})'.format(tree_text, children_text)

        return tree_text

    @classmethod
    def from_dict(cls, data):
        """Construct an instance from python built-in containers.

        Parameters
        ----------
            data : str
                A parse tree in dictionary format.
        """
        tree = cls()

        node_queue = _deque()
        node_queue.append((data, None,))

        while node_queue:
            node_dict, parent_id = node_queue.popleft()
            node_id = node_dict['id']
            node_data = cls.node_class.data_class.from_dict(node_dict['data'])
            tree.create_node(tag=node_data.to_text(), identifier=node_id, parent=parent_id, data=node_data)

            for child in node_dict['children']:
                node_queue.append((child, node_id,))

        return tree

    def to_dict(self, node_id=None):
        """Transform to python built-in containers.

        Parameters
        ----------
            node_id : int
                Output the plain text format for the subtree under **node_id**.

        Returns
        -------
            str
        """
        if node_id is None:
            node_id = self.root

        tree_dict = self[node_id].to_dict()
        tree_dict['children'] = []

        for child in self.children(node_id):
            tree_dict['children'].append(self.to_dict(child.identifier))

        return tree_dict

    @classmethod
    def from_penn(cls, data):
        """Construct an instance from Penn Treebank format."""
        tree = cls()

        node_stack = _deque()
        node_stack.append((data, None,))

        node_id = 0

        while node_stack:
            penn_data, parent_id = node_stack.pop()

            if not penn_data:
                raise SyntaxError(f'Empty node #{node_id}')

            if not isinstance(penn_data[0], str):
                raise SyntaxError(f'First element of a node must be string, got {type(penn_data[0])}')

            if len(penn_data) == 2 and isinstance(penn_data[-1], str):
                penn_data = (':'.join(penn_data),)

            node_data = cls.node_class.data_class.from_text(penn_data[0])
            tree.create_node(tag=node_data.to_text(), identifier=node_id, parent=parent_id, data=node_data)

            for child in penn_data[-1:0:-1]:
                node_stack.append((child, node_id,))
            node_id += 1

        return tree

    def to_penn(self, node_id=None, *, with_role=True, with_word=True, sep=':'):
        """Transform to Penn Treebank format.

        Parameters
        ----------
            node_id : int
                Output the plain text format for the subtree under **node_id**.
            with_role : bool
                Contains role-tag or not.
            with_word : bool
                Contains word or not.
            sep : str
                The seperator between role and POS-tag.

        Returns
        -------
            list
        """
        if node_id is None:
            node_id = self.root
        node = self[node_id]

        penn_data = [f'{node.data.role}{sep}{node.data.pos}' if with_role and node.data.role else node.data.pos,]
        if with_word and node.data.word:
            penn_data.append(node.data.word)

        for child in self.children(node_id):
            penn_data.append(self.to_penn(child.identifier, with_role=with_role, with_word=with_word, sep=sep))

        return penn_data

    ########################################################################################################################

    def show(self, *,
        key=lambda node: node.identifier,
        idhidden=False,
        **kwargs,
    ):
        """Show pretty tree."""
        _Tree.show(self, key=key, idhidden=idhidden, **kwargs)

    def get_children(self, node_id, *, role):
        """Get children of a node with given role.

        Parameters
        ----------
            node_id : int
                ID of target node.
            role : str
                the target role.

        Yields
        ------
            :class:`ParseNode`
                the children nodes with given role.
        """
        for child in self.children(node_id):
            if child.data.role == role:
                yield child

    def get_heads(self, root_id=None, *, semantic=True, deep=True):
        """Get all head nodes of a subtree.

        Parameters
        ----------
            root_id : int
                ID of the root node of target subtree.
            semantic : bool
                use semantic/syntactic policy. For semantic mode, return ``DUMMY`` or ``head`` instead of syntactic ``Head``.
            deep : bool
                find heads recursively.

        Yields
        ------
            :class:`ParseNode`
                the head nodes.
        """
        if root_id is None:
            root_id = self.root

        head_nodes = []
        children = list(self.children(root_id))

        # No child, choose the root node instead
        if not children:
            head_nodes.append(self[root_id])

        # Semantic mode
        if semantic:
            # Find DUMMY
            if not head_nodes:
                for child in children:
                    if child.data.role in ('DUMMY', 'DUMMY1', 'DUMMY2',):
                        head_nodes.append(child)

            # Find head
            if not head_nodes:
                for child in children:
                    if child.data.role == 'head':
                        head_nodes.append(child)

        # Find Head
        if not head_nodes:
            for child in children:
                if child.data.role == 'Head':
                    head_nodes.append(child)

        # Found no head, choose the last child instead
        if not head_nodes:
            head_nodes.append(children[-1])

        # Recursion
        for node in head_nodes:
            if deep and not node.is_leaf():
                yield from self.get_heads(node.identifier, semantic=semantic)
            else:
                yield node

    def get_relations(self, root_id=None, *, semantic=True):
        """Get all relations of a subtree.

        Parameters
        ----------
            root_id : int
                ID of the subtree root node.
            semantic : bool
                please refer :meth:`get_heads` for policy detail.

        Yields
        ------
            :class:`ParseRelation`
                the relations.
        """
        if root_id is None:
            root_id = self.root

        children = list(self.children(root_id))
        head_children = list(self.get_heads(root_id, semantic=semantic, deep=False))

        # Get heads
        for head_node in self.get_heads(root_id, semantic=semantic):
            # Get tails
            for tail in children:
                if tail.data.role != 'Head' and tail not in head_children:
                    if tail.is_leaf():
                        yield ParseRelation(  # pylint: disable=no-value-for-parameter
                            head=head_node, tail=tail, relation=tail,
                        )
                    else:
                        for node in self.get_heads(tail.identifier, semantic=semantic):
                            yield ParseRelation(  # pylint: disable=no-value-for-parameter
                                head=head_node, tail=node, relation=tail,
                            )

        # Recursion
        for child in children:
            yield from self.get_relations(child.identifier, semantic=semantic)

    def get_subjects(self, root_id=None, *, semantic=True, deep=True):
        """Get the subject node of a subtree.

        Parameters
        ----------
            root_id : int
                ID of the root node of target subtree.
            semantic : bool
                please refer :meth:`get_heads` for policy detail.
            deep : bool
                please refer :meth:`get_heads` for policy detail.

        Yields
        ------
            :class:`ParseNode`
                the subject node.

        Notes
        -----
            A node can be a subject if either:

            1. is a head of `NP`
            2. is a head of a subnode (`N`) of `S` with subject role
            3. is a head of a subnode (`N`) of `S` with neutral role and before the head (`V`) of `S`
        """
        if root_id is None:
            root_id = self.root
        root = self[root_id]

        if root.data.pos == 'NP':
            yield from self.get_heads(root.identifier, semantic=semantic, deep=deep)

        elif root.data.pos == 'S':
            for head in self.get_heads(root.identifier, semantic=False, deep=False):
                if head.data.pos.startswith('V'):
                    for subroot in self.children(root.identifier):
                        if subroot.data.pos.startswith('N') and ( \
                            subroot.data.role in _SUBJECT_ROLES or \
                           (subroot.data.role in _NEUTRAL_ROLES and subroot.identifier < head.identifier) \
                        ):
                            yield from self.get_heads(subroot.identifier, semantic=semantic, deep=deep)
