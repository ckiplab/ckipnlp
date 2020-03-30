#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

from enum import (
    IntEnum as _IntEnum,
    auto as _enum_auto,
)

from ckipnlp.driver import (
    CkipClassicWs as _CkipClassicWs,
    CkipClassicParser as _CkipClassicParser,
    CkipTaggerSeg as _CkipTaggerSeg,
    CkipTaggerPos as _CkipTaggerPos,
    CkipTaggerNer as _CkipTaggerNer,
)

################################################################################################################################

class DriverType(_IntEnum):
    CLASSIC = _enum_auto()
    TAGGER = _enum_auto()

################################################################################################################################

class CkipWorkspace:  # pylint: disable=too-few-public-methods

    def __init__(self, *, text=None, seg=None, ws=None, ner=None, parsed=None):
        self.text = text
        self.seg = seg
        self.ws = ws
        self.ner = ner
        self.parsed = parsed

    def __repr__(self):
        return str(self.__dict__)

    def items(self):
        return self.__dict__.items()

################################################################################################################################

class CkipPipeline:  # pylint: disable=too-few-public-methods

    def __init__(self, *, seg=None, pos=None, ner=None, parser=None):
        self._ws_driver = None
        self._seg_driver = None
        self._pos_driver = None
        self._parser_driver = None
        self._ner_driver = None

        # WordSeg
        if seg is None:
            pass
        elif seg == DriverType.CLASSIC:
            self._ws_driver = _CkipClassicWs()
        elif seg == DriverType.TAGGER:
            self._seg_driver = _CkipTaggerSeg()
        else:
            raise KeyError(f'Word segmentation is not implemented for type {seg.name}')

        # POS
        if pos is None:
            pass
        elif pos == DriverType.TAGGER:
            self._pos_driver = _CkipTaggerPos()
        else:
            raise KeyError(f'Part-of-speech tagging is not implemented for type {pos.name}')

        # Parser
        if parser is None:
            pass
        elif parser == DriverType.CLASSIC:
            self._parser_driver = _CkipClassicParser()
        else:
            raise KeyError(f'Sentence parsing is not implemented for type {parser.name}')

        # NER
        if ner is None:
            pass
        elif ner == DriverType.TAGGER:
            self._ner_driver = _CkipTaggerNer()
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

        workspace = CkipWorkspace(**feed)
        setattr(workspace, '_ws_tmp', None)
        for key in query:
            getattr(self, f'_get_{key}')(workspace)
        delattr(workspace, '_ws_tmp')
        return workspace

    ########################################################################################################################

    @staticmethod
    def _get_text(workspace):
        if workspace.text is None:
            raise AttributeError('text not exist!')
        return workspace.text

    ########################################################################################################################

    def _get_ws_tmp(self, workspace):
        if workspace._ws_tmp is None:  # pylint: disable=protected-access

            if self._ws_driver is not None:
                workspace._ws_tmp = self._ws_driver(  # pylint: disable=protected-access
                    text=self._get_text(workspace)
                )

            else:
                raise AttributeError('No classic word-segmentation driver!')

        return workspace._ws_tmp  # pylint: disable=protected-access

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

    def _get_parsed(self, workspace):
        if workspace.parsed is None:

            if self._parser_driver is not None:
                workspace.parsed = self._parser_driver(
                    ws=self._get_ws(workspace),
                )

            else:
                raise AttributeError('No sentence parsing driver!')

        return workspace.parsed
