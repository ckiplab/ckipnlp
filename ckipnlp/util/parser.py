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

import treelib as _treelib

################################################################################################################################

class ParserNodeData(NamedTuple):
    """A parser node."""

    role: str = None #: *str* – the role.
    pos: str = None  #: *str* – the post-tag.
    term: str = None #: *str* – the text term.

    def __str__(self):
        return self.to_text()

    @classmethod
    def from_text(cls, text):
        """Construct an instance from :class:`ckipnlp.parser.CkipParser` output.

        Parameters
        ----------
            data : str
                text such as ``'Head:Na:中文字'``.

        Notes
        -----
            - ``'Head:Na:中文字'`` -> role = ``'Head'``, pos = ``'Na'``, term = ``'中文字'``
            - ``'Head:Na'``       -> role = ``'Head'``, pos = ``'Na'``, term = ``None``
            - ``'Na'``            -> role = ``None``,   pos = ``'Na'``, term = ``None``
        """
        if ':' in text:
            fields = text.split(':')
            return cls(*fields)
        return cls(pos=text)

    def to_text(self):
        """Transform to plain text.

        Return
        ------
            str
        """
        return ':'.join(filter(None, self))

    @classmethod
    def from_dict(cls, data):
        """Construct an instance from python built-in containers.

        Parameters
        ----------
            data : dict
                dictionary such as ``{ 'role': 'Head', 'pos': 'Na', 'term': '中文字' }``
        """
        return cls(**data)

    def to_dict(self):
        """Transform to python built-in containers.

        Return
        ------
            dict
        """
        return self._asdict() # pylint: disable=no-member

    @classmethod
    def from_json(cls, data, **kwargs):
        """Construct an instance from JSON format.

        Parameters
        ----------
            data : str
                please refer :meth:`from_dict` for format details.
        """
        return cls.from_dict(_json.loads(data, **kwargs))

    def to_json(self, **kwargs):
        """Transform to JSON format.

        Return
        ------
            str
        """
        return _json.dumps(self.to_dict(), **kwargs)

class ParserNode(_treelib.Node):
    """A parser node for tree.

    Attributes
    ----------
        data : :class:`ParserNodeData`

    See Also
    --------
        treelib.tree.Node: Please refer `<https://treelib.readthedocs.io/>`_ for built-in usages.
    """

    data_class = ParserNodeData

    def __repr__(self):
        return '{name}(tag={tag}, identifier={identifier})'.format(
            name=self.__class__.__name__,
            tag=self.tag,
            identifier=self.identifier,
        )

    def to_dict(self):
        """Transform to python built-in containers.

        Return
        ------
            dict
        """
        return _collections.OrderedDict(id=self.identifier, data=self.data.to_dict())

    def to_json(self, **kwargs):
        """Transform to JSON format.

        Return
        ------
            str
        """
        return _json.dumps(self.to_dict(), **kwargs)

class ParserRelation(NamedTuple):
    """A parser relation."""

    head: ParserNode #: :class:`ParserNode` – the head node.
    tail: ParserNode #: :class:`ParserNode` – the tail node.
    relation: str #: *str* – the relation.

    def __repr__(self):
        ret = '{name}(head={head}, tail={tail}, relation={relation})' if self._head_first \
         else '{name}(tail={tail}, head={head}, relation={relation})'
        return ret.format(name=type(self).__name__, head=self.head, tail=self.tail, relation=self.relation)

    @property
    def _head_first(self):
        return self.head.identifier <= self.tail.identifier

    def to_dict(self):
        """Transform to python built-in containers.

        Return
        ------
            dict
        """
        return _collections.OrderedDict(head=self.head.to_dict(), tail=self.head.to_dict(), relation=self.relation)

    def to_json(self, **kwargs):
        """Transform to JSON format.

        Return
        ------
            str
        """
        return _json.dumps(self.to_dict(), **kwargs)

################################################################################################################################

class ParserTree(_treelib.Tree):
    """A parsed tree.

    See Also
    --------
    treereelib.tree.Tree: Please refer `<https://treelib.readthedocs.io/>`_ for built-in usages.
    """

    node_class = ParserNode

    @staticmethod
    def normalize_text(tree_text):
        """Text normalization for :class:`ckipnlp.parser.CkipParser` output.

        Remove leading number and trailing ``#``.
        """
        if '#' in tree_text:
            tree_text = tree_text.split('] ', 2)[-1].rstrip('#')
        return tree_text

    def __str__(self):
        self.to_text()

    @classmethod
    def from_text(cls, tree_text, *, normalize=True):
        """Create a :class:`ParserTree` object from :class:`ckipnlp.parser.CkipParser` output.

        Parameters
        ----------
            text : str
                A parsed tree from :class:`ckipnlp.parser.CkipParser` output.
            normalize : bool
                Do text normalization using :meth:`normalize_text`.
        """
        if normalize:
            tree_text = cls.normalize_text(tree_text)

        tree = cls()
        node_id = 0
        node_queue = [None]
        text = ''
        ending = True

        for char in tree_text:
            if char == '(':
                node_data = cls.node_class.data_class.from_text(text)
                tree.create_node(tag=text, identifier=node_id, parent=node_queue[-1], data=node_data)

                node_queue.append(node_id)
                node_id += 1
                text = ''

            elif char == ')':
                if not ending:
                    node_data = cls.node_class.data_class.from_text(text)
                    tree.create_node(tag=text, identifier=node_id, parent=node_queue[-1], data=node_data)
                    node_id += 1

                node_queue.pop()
                text = ''
                ending = True

            elif char == '|':
                if not ending:
                    node_data = cls.node_class.data_class.from_text(text)
                    tree.create_node(tag=text, identifier=node_id, parent=node_queue[-1], data=node_data)
                    node_id += 1

                text = ''
                ending = True

            else:
                ending = False
                text += char

        return tree

    def to_text(self, node_id=0):
        """Transform to plain text.

        Return
        ------
            str
        """
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
            data : dict
                dictionary such as ``{ 'id': 0, 'data': { ... }, 'children': [ ... ] }``,
                where ``'data'`` is a dictionary with the same format as :meth:`ParserNodeData.to_dict`,
                and ``'children'`` is a list of dictionaries of subtrees with the same format as this tree.
        """
        tree = cls()

        queue = _collections.deque()
        queue.append((data, None,))

        while queue:
            node_dict, parent_id = queue.popleft()
            node_id = node_dict['id']
            node_data = cls.node_class.data_class.from_dict(node_dict['data'])
            tree.create_node(tag=node_data.to_text(), identifier=node_id, parent=parent_id, data=node_data)

            for child in node_dict['children']:
                queue.append((child, node_id,))

        return tree

    def to_dict(self, node_id=0): # pylint: disable=arguments-differ
        """Transform to python built-in containers.

        Return
        ------
            dict
        """
        tree_dict = self[node_id].to_dict()
        tree_dict['children'] = []

        for child in self.children(node_id):
            tree_dict['children'].append(self.to_dict(child.identifier))

        return tree_dict

    @classmethod
    def from_json(cls, data, **kwargs):
        """Construct an instance from JSON format.

        Parameters
        ----------
            data : str
                please refer :meth:`from_dict` for format details.
        """
        return cls.from_dict(_json.loads(data, **kwargs))

    def to_json(self, node_id=0, **kwargs): # pylint: disable=arguments-differ
        """Transform to JSON format.

        Return
        ------
            str
        """
        return _json.dumps(self.to_dict(node_id=node_id), **kwargs)

    def show(self, *, # pylint: disable=arguments-differ
        key=lambda node: node.identifier,
        idhidden=False,
        **kwargs,
    ):
        """Show pretty tree."""
        super().show(key=key, idhidden=idhidden, **kwargs)

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
            :class:`ParserNode`
                the children nodes with given role.
        """
        for child in self.children(node_id):
            if child.data.role == role:
                yield child

    def get_heads(self, root_id=0, *, semantic=True, deep=True): # pylint: disable=too-many-branches
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
            :class:`ParserNode`
                the head nodes.
        """
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

    def get_relations(self, root_id=0, *, semantic=True):
        """Get all relations of a subtree.

        Parameters
        ----------
            root_id : int
                ID of the subtree root node.
            semantic : bool
                please refer :meth:`get_heads` for policy detail.

        Yields
        ------
            :class:`ParserRelation`
                the relations.
        """

        children = list(self.children(root_id))
        head_children = list(self.get_heads(root_id, semantic=semantic, deep=False))

        # Get heads
        for head_node in self.get_heads(root_id, semantic=semantic):
            # Get tails
            for tail in children:
                if tail.data.role != 'Head' and tail not in head_children:
                    if tail.is_leaf():
                        yield ParserRelation(head=head_node, tail=tail, relation=tail.data.role)
                    else:
                        for node in self.get_heads(tail.identifier, semantic=semantic):
                            yield ParserRelation(head=head_node, tail=node, relation=tail.data.role)

        # Recursion
        for child in children:
            yield from self.get_relations(child.identifier, semantic=semantic)
