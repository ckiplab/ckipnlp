#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import collections as _collections
import itertools as _itertools
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

    @classmethod
    def from_text(cls, text):
        """Create a :class:`ParserNodeData` object from :class:`ckipnlp.parser.CkipParser` output."""
        fields = text.split(':')
        return cls(*fields)

    def __str__(self):
        return self.to_text()

    def to_text(self):
        """Transform to plain text."""
        return ':'.join(filter(None, self))

    def to_dict(self):
        """Transform to python dict/list."""
        return self._asdict() # pylint: disable=no-member

    def to_json(self, **kwargs):
        """Transform to JSON format."""
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

    def __repr__(self):
        return '{name}(tag={tag}, identifier={identifier})'.format(
            name=self.__class__.__name__,
            tag=self.tag,
            identifier=self.identifier,
        )

    def to_text(self):
        """Transform to plain text."""
        return self.data.to_text()

    def to_dict(self):
        """Transform to python dict/list."""
        return _collections.OrderedDict(id=self.identifier, **self.data.to_dict())

    def to_json(self, **kwargs):
        """Transform to JSON format."""
        return _json.dumps(self.to_dict(), **kwargs)

class ParserRelation(NamedTuple):
    """A parser relation."""

    head: ParserNode #: :class:`ParserNode` – the head node.
    tail: ParserNode #: :class:`ParserNode` – the tail node.
    relation: str #: *str* – the relation.

    def __repr__(self):
        ret = '{name}(head={head}, tail={tail}, relation={relation})' if self.head_first \
         else '{name}(tail={tail}, head={head}, relation={relation})'
        return ret.format(name=type(self).__name__, head=self.head, tail=self.tail, relation=self.relation)

    @property
    def head_first(self):
        return self.head.identifier <= self.tail.identifier

    def to_dict(self):
        """Transform to python dict/list."""
        return _collections.OrderedDict(head=self.head.to_dict(), tail=self.head.to_dict(), relation=self.relation)

    def to_json(self, **kwargs):
        """Transform to JSON format."""
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

        Remove leading number and trailing ``#``. Prepend ``root:`` at beginning.
        """
        return 'root:' + tree_text.split(' ', 2)[-1].split('#')[0]

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
                node_data = ParserNodeData.from_text(text)
                tree.create_node(tag=text, identifier=node_id, parent=node_queue[-1], data=node_data)

                node_queue.append(node_id)
                node_id += 1
                text = ''

            elif char == ')':
                if not ending:
                    node_data = ParserNodeData.from_text(text)
                    tree.create_node(tag=text, identifier=node_id, parent=node_queue[-1], data=node_data)
                    node_id += 1

                node_queue.pop()
                text = ''
                ending = True

            elif char == '|':
                if not ending:
                    node_data = ParserNodeData.from_text(text)
                    tree.create_node(tag=text, identifier=node_id, parent=node_queue[-1], data=node_data)
                    node_id += 1

                text = ''
                ending = True

            else:
                ending = False
                text += char

        return tree

    def __str__(self):
        self.to_text()

    def to_text(self, node_id=0):
        """Transform to plain text."""
        node = self[node_id]
        tree_text = node.to_text()

        children_text = '|'.join((self.to_text(child.identifier) for child in self.children(node_id)))
        if children_text:
            tree_text = '{}({})'.format(tree_text, children_text)

        return tree_text

    def to_dict(self, node_id=0): # pylint: disable=arguments-differ
        """Transform to python dict/list."""
        node = self[node_id]
        tree_dict = node.to_dict()

        for child in self.children(node_id):
            tree_dict.setdefault('children', list()).append(self.to_dict(child.identifier))

        return tree_dict

    def to_json(self, **kwargs): # pylint: disable=arguments-differ
        """Transform to JSON format."""
        return _json.dumps(self.to_dict(), **kwargs)

    def show(self, *, # pylint: disable=arguments-differ
        key=lambda node: node.identifier,
        idhidden=False,
        **kwargs,
    ):
        """Show pretty tree."""
        super().show(key=key, idhidden=idhidden, **kwargs)

    def has_dummies(self, node_id):
        """Determine if a node has dummies.

        Parameters
        ----------
            node_id : int
                ID of target node.

        Returns
        -------
            bool
                whether or not target node has dummies.
        """
        roles = [node.data.role for node in self.children(node_id)]
        return 'DUMMY1' in roles and 'DUMMY2' in roles

    def get_dummies(self, node_id, deep=True, _check=True):
        """Get dummies of a node.

        Parameters
        ----------
            node_id : int
                ID of target node.
            deep : bool
                find dummies recursively.

        Returns
        -------
            Tuple[:class:`ParserNode`]
                the dummies.

        Raises
        ------
            LookupError
                when target node has no dummy (only when **_check** is set).
        """
        if _check and not self.has_dummies(node_id):
            raise LookupError('Node ({node_id}) does not have dummies!'.format(node_id=node_id))

        dummy1 = ()
        dummy2 = ()

        for child in self.children(node_id):

            if child.data.role == 'DUMMY1':
                if deep and self.has_dummies(child.identifier):
                    dummy1 = self.get_dummies(child.identifier, deep=True, _check=False)
                else:
                    dummy1 = (child,)

            if child.data.role == 'DUMMY2':
                if deep and self.has_dummies(child.identifier):
                    dummy2 = self.get_dummies(child.identifier, deep=True, _check=False)
                else:
                    dummy2 = (child,)

        return (*dummy1, *dummy2,)

    def get_heads(self, root_id=0, deep=True): # pylint: disable=too-many-branches
        """Get all head nodes of a subtree.

        Parameters
        ----------
            root_id : int
                ID of the root node of target subtree.
            deep : bool
                find heads recursively.

        Returns
        -------
            List[:class:`ParserNode`]
                the head nodes (when **deep** is set).
            :class:`ParserNode`
                the head node (when **deep** is not set).

        Todo
        ----
            Get information of nodes with pos type PP or GP.
        """
        head_nodes = None
        children = list(self.children(root_id))

        # No child, choose the root node instead
        if not children:
            head_nodes = (self[root_id],)

        # Find head
        if head_nodes is None:
            for child in children:
                if child.data.role == 'head':
                    if not deep:
                        head_nodes = (child,)
                    else:
                        if child.data.pos == 'Caa': # Found Caa, choose dummies of root instead
                            head_nodes = tuple(_itertools.chain.from_iterable(
                                self.get_heads(node.identifier) for node in self.get_dummies(root_id, _check=False)
                            ))
                        else:
                            head_nodes = self.get_heads(child.identifier)
                    break

        # Find Head
        if head_nodes is None:
            for child in children:
                if child.data.role == 'Head':
                    if not deep:
                        head_nodes = (child,)
                    else:
                        if child.data.pos == 'Caa': # Found Caa, choose dummies of root instead
                            head_nodes = tuple(_itertools.chain.from_iterable(
                                self.get_heads(node.identifier) for node in self.get_dummies(root_id, _check=False)
                            ))
                        else:
                            head_nodes = self.get_heads(child.identifier)
                    break

        # Found no head, choose the last child instead
        if head_nodes is None:
            head_nodes = (children[-1],)

        return head_nodes[0] if not deep else head_nodes

    def get_relations(self, root_id=0):
        """Get all relations of a subtree.

        Parameters
        ----------
            root_id : int
                ID of the subtree root node.

        Yields
        ------
            :class:`ParserRelation`
                the relation.
        """

        head_root_node = self.get_heads(root_id, deep=False)

        # Skip Caa
        if head_root_node.data.pos == 'Caa':
            return

        # Get heads
        for head_node in self.get_heads(root_id):

            # Get tails
            for tail in self.children(root_id):
                if tail.identifier != head_root_node.identifier:
                    if tail.data.term: # if tail is a leaf node
                        yield ParserRelation(head=head_node, tail=tail, relation=tail.data.role)
                    else:
                        for node in self.get_heads(tail.identifier):
                            yield ParserRelation(head=head_node, tail=node, relation=tail.data.role)

        # Recursion
        for child in self.children(root_id):
            yield from self.get_relations(child.identifier)
