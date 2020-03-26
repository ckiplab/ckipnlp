#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from enum import (
    IntEnum as _IntEnum,
    auto as _enum_auto,
)

from typing import (
    NamedTuple as _NamedTuple,
)

import ckipnlp.container as _container
import ckipnlp.driver as _driver

################################################################################################################################

class DriverType(_IntEnum):
    CLASSICAL = _enum_auto()
    TAGGER = _enum_auto()

################################################################################################################################

class Workspace:

    def __init__(self, *, text=None, seg=None, ws=None, ner=None, parser=None):
        self.text = text
        self.seg = seg
        self.ws = ws
        self.ner = ner
        self.parser = parser

    def __repr__(self):
        return str(self.__dict__)

################################################################################################################################

class CkipPipeline:

    def __init__(self, *, seg=None, pos=None, ner=None, parser=None):
        self._ws_driver = None
        self._seg_driver = None
        self._pos_driver = None
        self._parser_driver = None
        self._ner_driver = None

        # WordSeg
        if seg is None:
            pass
        elif seg == DriverType.CLASSICAL:
            self._ws_driver = _driver.CkipClassicalWs()
        elif seg == DriverType.TAGGER:
            self._seg_driver = _driver.CkipTaggerSeg()
        else:
            raise KeyError(f'Word segmentation is not implemented for type {seg.name}')

        # POS
        if pos is None:
            pass
        elif pos == DriverType.TAGGER:
            self._pos_driver = _driver.CkipTaggerPos()
        else:
            raise KeyError(f'Part-of-speech tagging is not implemented for type {pos.name}')

        # Parser
        if parser is None:
            pass
        elif parser == DriverType.CLASSICAL:
            self._parser_driver = _driver.CkipClassicalParser()
        else:
            raise KeyError(f'Sentence parsing is not implemented for type {parser.name}')

        # NER
        if ner is None:
            pass
        elif ner == DriverType.TAGGER:
            self._ner_driver = _driver.CkipTaggerNer()
        else:
            raise KeyError(f'Named entity recognition is not implemented for type {ner.name}')

    def __call__(self, **feed_query):
        feed = {}
        query = []
        for key, value in feed_query.items():
            if value is True:
                query.append(key)
            elif value is not None:
                feed[key] = value

        workspace = Workspace(**feed)
        workspace._ws_tmp = None
        for key in query:
            getattr(self, f'_get_{key}')(workspace)
        del workspace._ws_tmp
        return workspace

    ########################################################################################################################

    @staticmethod
    def _get_text(workspace):
        if workspace.text is None:
            raise AttributeError('text not exist!')
        return workspace.text

    ########################################################################################################################

    def _get_ws_tmp(self, workspace):
        if workspace._ws_tmp is None:

            if self._ws_driver is not None:
                workspace._ws_tmp = self._ws_driver(
                    text=self._get_text(workspace)
                )

            else:
                raise AttributeError('No classical word-segmentation driver!')

        return workspace._ws_tmp

    ########################################################################################################################

    def _get_seg(self, workspace):
        if workspace.seg is None:

            if self._seg_driver is not None:
                workspace.seg = self._seg_driver(
                    text=self._get_text(workspace)
                )

            elif self._ws_driver is not None:
                workspace.seg = f'<-pos {self._get_ws_tmp(workspace)}>'

            else:
                raise AttributeError('No word segmentation driver!')

        return workspace.seg

    ########################################################################################################################

    def _get_ws(self, workspace):
        if workspace.ws is None:

            if self._pos_driver is not None:
                workspace.ws = self._pos_driver(
                    seg=self._get_seg(workspace)
                )

            elif self._ws_driver is not None:
                workspace.ws = self._get_ws_tmp(workspace)

            else:
                raise AttributeError('No part-of-speech tagging driver!')

        return workspace.ws

    ########################################################################################################################

    def _get_ner(self, workspace):
        if workspace.ner is None:

            if self._ner_driver is not None:
                workspace.ner = self._ner_driver(
                    ws=self._get_ws(workspace),
                )

            else:
                raise AttributeError('No named entity recognition driver!')

        return workspace.ner

    ########################################################################################################################

    def _get_parser(self, workspace):
        if workspace.parser is None:

            if self._parser_driver is not None:
                workspace.parser = self._parser_driver(
                    ws=self._get_ws(workspace),
                )

            else:
                raise AttributeError('No named entity recognition driver!')

        return workspace.parser
