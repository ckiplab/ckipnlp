#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2018-2019'

import collections as _collections
import itertools as _itertools
import json as _json

import treelib as _treelib

################################################################################################################################

_ParserNodeData = _collections.namedtuple('_ParserNodeData', ('role', 'pos', 'term',))
_ParserNodeData.__new__.__defaults__ = (None, None, None,)
class ParserNodeData(_ParserNodeData):
    """A parser node.

    Fields:
        * **role** (*str*): the role.
        * **pos** (*str*): the post-tag.
        * **term** (*str*): the text term.
    """

    @classmethod
    def from_text(cls, text):
        """Create :class:`ParserNodeData` object from :class:`ckipnlp.parser.CkipParser` output."""
        fields = text.split(':')
        return cls(*fields)

    def to_dict(self):
        return self._asdict()

    def to_json(self, **kwargs):
        return _json.dumps(self.to_dict(), **kwargs)

class ParserNode(_treelib.Node):
    """A parser node for tree."""

    def to_dict(self):
        return _collections.OrderedDict(id=self.identifier, **self.data.to_dict())

    def to_json(self, **kwargs):
        return _json.dumps(self.to_dict(), **kwargs)

_ParserRelation = _collections.namedtuple('_ParserRelation', ('head', 'tail', 'relation'))
class ParserRelation(_ParserRelation):
    """A parser relation.

    Fields:
        * **head** (:class:`ParserNode`): the head node.
        * **tail** (:class:`ParserNode`): the tail node.
        * **relation** (str): the relation.
        """

    def __str__(self):
        ret = '{name}(head={head}, tail={tail}, relation={relation})' if self.head.identifier <= self.tail.identifier \
         else '{name}(tail={tail}, head={head}, relation={relation})'
        return ret.format(name=type(self).__name__, head=self.head, tail=self.tail, relation=self.relation)

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return _collections.OrderedDict(head=self.head.to_dict(), tail=self.head.to_dict(), relation=self.relation)

    def to_json(self, **kwargs):
        return _json.dumps(self.to_dict(), **kwargs)

################################################################################################################################

class ParserTree(_treelib.Tree):
    """A parsed tree."""

    @classmethod
    def from_text(cls, tree_text):
        """Create :class:`ParserTree` object from :class:`ckipnlp.parser.CkipParser` output."""
        tree = cls(node_class=ParserNode)

        if '#' in tree_text:
            tree_text = tree_text.split(' ', 2)[-1].split('#')[0]

        node_id = 0
        node_queue = [None]
        text = 'root:'
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

    def to_dict(self, node_id=0):
        node = self.get_node(node_id)
        tree_dict = node.to_dict()

        for child in self.children(node_id):
            tree_dict.setdefault('children', list()).append(self.to_dict(child.identifier))

        return tree_dict

    def to_json(self, **kwargs):
        return _json.dumps(self.to_dict(), **kwargs)

    def show(self, *, key=lambda node: node.identifier, idhidden=False, **kwargs): # pylint: disable=arguments-differ
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
        tuple
            the dummies (:class:`ParserNode`).

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
        node_id : int
            ID of the root node of target subtree.
        deep : bool
            find heads recursively.

        Returns
        -------
        list
            the head nodes (:class:`ParserNode`).
        :class:`ParserNode`
            the head node (when **deep** is set).

        Todo
        ----
        Get information of nodes with pos type PP or GP.
        """
        head_nodes = None
        children = list(self.children(root_id))

        # No child, choose the root node instead
        if not children:
            head_nodes = (self.get_node(root_id),)

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
        node_id : int
            ID of the subtree root node.

        Yields
        ------
        :class:`ParserRelation`
            the relation.
        """

        root_node = self.get_node(root_id)
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
