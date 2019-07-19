#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2018-2019'

import collections as _collections

import treelib as _treelib

_ParserNode = _collections.namedtuple('_ParserNode', ['role', 'pos', 'term'])
_ParserNode.__new__.__defaults__ = (None, None, None,)
class ParserNode(_ParserNode):
    """A parser node.

        Fields:
            * role: the role.
            * pos: the post-tag.
            * term: the text term.
    """

    @classmethod
    def from_text(cls, text):
        fields = text.split(':')
        return cls(*fields)

class ParserTree(_treelib.Tree):
    """A parsed tree."""

    @classmethod
    def from_text(cls, tree_text):
        """Create :class:`ParserTree` object from :class:`ckipnlp.ws.CkipParser` output."""

        tree = cls()

        node_id = 0
        node_queue = [None]
        text = 'root:'
        ending = True

        for char in tree_text:
            if char == '(':
                node_data = ParserNode.from_text(text)
                tree.create_node(tag=text, identifier=node_id, parent=node_queue[-1], data=node_data)

                node_queue.append(node_id)
                node_id += 1
                text = ''

            elif char == ')':
                if ending: continue
                node_data = ParserNode.from_text(text)
                tree.create_node(tag=text, identifier=node_id, parent=node_queue[-1], data=node_data)

                node_queue.pop()
                node_id += 1
                text = ''
                ending = True

            elif char == '|':
                if ending: continue
                node_data = ParserNode.from_text(text)
                tree.create_node(tag=text, identifier=node_id, parent=node_queue[-1], data=node_data)

                node_id += 1
                text = ''
                ending = True

            else:
                ending = False
                text += char

        return tree

    def show(self, *, key=lambda node: node.identifier, **kwargs):
        """Show pretty tree."""
        super().show(key=key, **kwargs)

    def has_dummies(self, node_id):
        """"""
        roles = [node.data.role for node in self.children(node_id)]
        return 'DUMMY1' in roles and 'DUMMY2' in roles
