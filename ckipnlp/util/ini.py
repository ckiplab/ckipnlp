#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2018-2019'

import datetime as _datetime
import os as _os
import sys as _sys
import warnings as _warnings

import ckipnlp as _about

def create_ws_ini( # pylint: disable=too-many-statements
        *,
        data2dir=None,
        lexfile=None,
        new_style_format=False,
        show_category=True,
        sentence_max_word_num=80,
        **options,
):
    """Generate CKIP word segmentation config.

    Parameters
    ----------
    data2dir : str
        the path to the folder "Data2/".
    lexfile : str
        the path to the user-defined lexicon file.

    new_style_format : bool
        split sentences by newline characters ("\\\\n") rather than punctuations.
    show_category : bool
        show part-of-speech tags.

    sentence_max_word_num : int
        maximum number of words per sentence.
    """

    # pylint: disable=invalid-name

    if data2dir is None:
        data2dir = _os.getenv('CKIPWS_DATA2')
        if not data2dir:
            data2dir = _os.path.join(_sys.prefix, 'share', 'ckipnlp', 'Data2')
        if not _os.path.isdir(data2dir):
            _warnings.warn('Invalid data2dir (%s)' % data2dir)
            data2dir = 'Data2'

    cfg = []

    cfg.append(';PyCkip {version}'.format(version=_about.__version__))
    cfg.append(';ws.ini')
    cfg.append(';Auto-generated {date}'.format(date=_datetime.datetime.now()))
    cfg.append('')

    cfg.append('[ConsoleLogger]')
    cfg.append('Name=ConsoleLogger')
    cfg.append('')

    if lexfile:
        cfg.append('[CTextLexicon]')
        cfg.append('Name=TextLex')
        cfg.append('FileName={lexfile}'.format(lexfile=lexfile))
        cfg.append('')

    cfg.append('[CLexicon]')
    cfg.append('Name=Lex')
    cfg.append('FileName={data2dir}/Lexicon.Dat'.format(data2dir=data2dir))
    cfg.append('')

    cfg.append('[CALexicon]')
    cfg.append('Name=CALex')
    cfg.append('FileName={data2dir}/CALexicon.Dat'.format(data2dir=data2dir))
    cfg.append('')

    cfg.append('[CDMMergedParser]')
    cfg.append('Name=DMMergedParser')
    cfg.append('GenerateMaxLengthWordOnly=no')
    cfg.append('LexiconName=Lex')
    cfg.append('')

    cfg.append('[CDMSplittedParser]')
    cfg.append('Name=DMSplittedParser')
    cfg.append('GenerateMaxLengthWordOnly=no')
    cfg.append('LexiconName=Lex')
    cfg.append('')

    cfg.append('[CHTRDRule3]')
    cfg.append('Name=RD3')
    cfg.append('LexiconName=Lex')
    cfg.append('')

    cfg.append('[CHTRDRule6]')
    cfg.append('Name=RD6')
    cfg.append('LexiconName=Lex')
    cfg.append('')

    cfg.append('[CHTRDRule7]')
    cfg.append('Name=RD7')
    cfg.append('LexiconName=Lex')
    cfg.append('')

    cfg.append('[CHTForeignWord]')
    cfg.append('Name=FW')
    cfg.append('LexiconName=Lex')
    cfg.append('')

    cfg.append('[CHTBoundWord]')
    cfg.append('Name=BW')
    cfg.append('LexiconName=Lex')
    cfg.append('')

    cfg.append('[CMaxMatch]')
    cfg.append('Name=MaxMatch')
    cfg.append('WindowSize=3')
    cfg.append('')

    cfg.append('[CHTCategoryPredictor]')
    cfg.append('Name=CatPred')
    cfg.append('PrefixCategoryFileName={data2dir}/CatPredictData/PrefixCategoryFreq'.format(data2dir=data2dir))
    cfg.append('PrefixFileName={data2dir}/CatPredictData/PrefixFreq'.format(data2dir=data2dir))
    cfg.append('SuffixCategoryFileName={data2dir}/CatPredictData/SuffixCategoryFreq'.format(data2dir=data2dir))
    cfg.append('SuffixFileName={data2dir}/CatPredictData/SuffixFreq'.format(data2dir=data2dir))
    cfg.append('')

    cfg.append('[CStatProb]')
    cfg.append('Name=CAProb1')
    cfg.append('FileName={data2dir}/CAStat-w(0)c(0)-w(-1).dat'.format(data2dir=data2dir))
    cfg.append('')

    cfg.append('[CStatProb]')
    cfg.append('Name=CAProb2')
    cfg.append('FileName={data2dir}/CAStat-w(0)c(0)-w(1).dat'.format(data2dir=data2dir))
    cfg.append('')

    cfg.append('[CStatProb]')
    cfg.append('Name=CAProb3')
    cfg.append('FileName={data2dir}/CAStat-w(0)c(0)-w(-2).dat'.format(data2dir=data2dir))
    cfg.append('')

    cfg.append('[CStatProb]')
    cfg.append('Name=CAProb4')
    cfg.append('FileName={data2dir}/CAStat-w(0)c(0)-w(2).dat'.format(data2dir=data2dir))
    cfg.append('')

    cfg.append('[CoveringAmbiguity]')
    cfg.append('Name=CA')
    cfg.append('LexiconName=Lex')
    cfg.append('CoveringAmbiguityLexiconName=CALex')
    cfg.append('InsertSplittedWordsOnly=false')
    cfg.append('StatisticProbability1=CAProb1')
    cfg.append('StatisticProbability2=CAProb2')
    cfg.append('StatisticProbability3=CAProb3')
    cfg.append('StatisticProbability4=CAProb4')
    cfg.append('')

    cfg.append('[CStatProb]')
    cfg.append('Name=Prob1')
    cfg.append('FileName={data2dir}/CKIPWStatistic-w(-1)-w(0).dat'.format(data2dir=data2dir))
    cfg.append('')

    cfg.append('[CStatProb]')
    cfg.append('Name=Prob2')
    cfg.append('FileName={data2dir}/CKIPWStatistic-c(-1)-c(0).dat'.format(data2dir=data2dir))
    cfg.append('')

    cfg.append('[CStatProb]')
    cfg.append('Name=Prob3')
    cfg.append('FileName={data2dir}/CKIPWStatistic-c(0)-w(0).dat'.format(data2dir=data2dir))
    cfg.append('')

    cfg.append('[CSimpleProbModel]')
    cfg.append('Name=ProbModel')
    cfg.append('StatisticProbability1=Prob1')
    cfg.append('StatisticProbability2=Prob2')
    cfg.append('StatisticProbability3=Prob3')
    cfg.append('LexiconName=Lex')
    if lexfile:
        cfg.append('TextLexiconName=TextLex')
    cfg.append('AdjustProb3=true')
    cfg.append('CoveringAmbiguityLexiconName=CALex')
    cfg.append('CategoryPredictor=CatPred')
    cfg.append('KeepBestCategory=true')
    cfg.append('SimplifiedCategory=false')
    cfg.append('')

    cfg.append('[CDetectMonosyllabicMorpheme]')
    cfg.append('Name=DMM')
    cfg.append('ApplyDefaultHeuristicDetectRule=yes')
    cfg.append('InitDataPath={data2dir}/uwea/qrulepool/'.format(data2dir=data2dir))
    cfg.append('')

    cfg.append('[ChineseName]')
    cfg.append('Name=CN')
    cfg.append('LexiconName=Lex')
    cfg.append('InitDataPath={data2dir}/uwea/data/'.format(data2dir=data2dir))
    cfg.append('')

    cfg.append('[CForeignName]')
    cfg.append('Name=FN')
    cfg.append('LexiconName=Lex')
    if lexfile:
        cfg.append('TextLexiconName=TextLex')
    cfg.append('InitDataPath={data2dir}/uwea/data/'.format(data2dir=data2dir))
    cfg.append('')

    cfg.append('[CompoundWord]')
    cfg.append('Name=CW')
    cfg.append('LexiconName=Lex')
    cfg.append('InitDataPath={data2dir}/uwea/data/'.format(data2dir=data2dir))
    cfg.append('')

    cfg.append('[CStatisticWord]')
    cfg.append('Name=SW')
    cfg.append('LexiconName=Lex')
    if lexfile:
        cfg.append('TextLexiconName=TextLex')
    cfg.append('CategoryPredictor=CatPred')
    cfg.append('InitDataPath={data2dir}/uwea/data/'.format(data2dir=data2dir))
    cfg.append('ApplyRule=639')
    cfg.append('')

    cfg.append('[CAffixCombiner]')
    cfg.append('Name=AC')
    cfg.append('LexiconName=Lex')
    if lexfile:
        cfg.append('TextLexiconName=TextLex')
    cfg.append('CategoryPredictor=CatPred')
    cfg.append('')

    cfg.append('[CSimilarStructureCombiner]')
    cfg.append('Name=SSC')
    cfg.append('AutoCombineWordLen=2')
    cfg.append('HeuristicCombinedWordMaxLen=3')
    cfg.append('LexiconName=Lex')
    cfg.append('CategoryPredictor=CatPred')
    cfg.append('')

    cfg.append('[COnlineLexicon]')
    cfg.append('Name=OnlineLexForUWGen')
    cfg.append('')

    cfg.append('[CUnknownWord]')
    cfg.append('Name=UW')
    cfg.append('UnknownWordGeneratorList=DMM CN FN CW SW SSC')
    cfg.append('OnlineLexicon=OnlineLexForUWGen')
    cfg.append('')

    if lexfile:
        cfg.append('[CLexWordGenerator]')
        cfg.append('Name=myLWGen')
        cfg.append('LexiconName=TextLex')
        cfg.append('')

    cfg.append('[CLexWordGenerator]')
    cfg.append('Name=LWGen')
    cfg.append('LexiconName=Lex')
    cfg.append('')

    cfg.append('[CLexWordGenerator]')
    cfg.append('Name=LWGen1')
    cfg.append('LexiconName=Lex')
    cfg.append('MaxWordLen=1')
    cfg.append('')

    cfg.append('[CLexWordGenerator]')
    cfg.append('Name=UWGen')
    cfg.append('LexiconName=OnlineLexForUWGen')
    cfg.append('')

    cfg.append('[CSimpleProbModelResult]')
    cfg.append('Name=ProbModelResult')
    cfg.append('ProbabilityModelName=ProbModel')
    cfg.append('NewStyleFormat={NewStyleFormat}'.format(NewStyleFormat=str(new_style_format).lower()))
    cfg.append('ShowCategory={ShowCategory}'.format(ShowCategory=str(show_category).lower()))
    cfg.append('LexiconName=Lex')
    cfg.append('CategoryPredictor=CatPred')
    cfg.append('KeepExistingWord=true')
    cfg.append('FeatureAssigner=FA')
    cfg.append('FilterBadWord=false')
    cfg.append('')

    cfg.append('[CDetectDMForPostProcess]')
    cfg.append('Name=DDMFPP')
    cfg.append('')

    cfg.append('[CRemoveWordToBePostProcessed]')
    cfg.append('Name=RWTBPP')
    cfg.append('')

    HandlerList = [
        'LWGen', 'myLWGen', 'DMMergedParser', 'RD3', 'RD6', 'RD7', 'FW', 'BW', 'MaxMatch', 'ProbModel', 'UW', 'DDMFPP',
        'LWGen', 'UWGen', 'RWTBPP', 'LWGen', 'myLWGen', 'DMSplittedParser', 'BW', 'MaxMatch', 'ProbModel', 'CA'
    ]

    if not lexfile:
        while 'myLWGen' in HandlerList:
            HandlerList.remove('myLWGen')

    cfg.append('[CWordSegmentor]')
    cfg.append('Name=MainWS')
    cfg.append('ArticleMaxLineNum=300')
    cfg.append('SentenceMaxWordNum={sentence_max_word_num}'.format(sentence_max_word_num=sentence_max_word_num))
    cfg.append('ReloadMyDic=false')
    cfg.append('SentenceDelimiter=，,；。！？')
    cfg.append('HandlerList={HandlerList}'.format(HandlerList=' '.join(HandlerList)))
    cfg.append('Result=ProbModelResult')
    cfg.append('')

    return '\n'.join(cfg), options

def create_parser_ini( # pylint: disable=too-many-statements
        *,
        wsinifile,
        ruledir=None,
        rdbdir=None,
        do_ws=True,
        do_parse=True,
        do_role=True,
        sentence_delim='，,；。！？',
        **options,
):
    """Generate CKIP parser config.

    Parameters
    ----------
    ruledir : str
        the path to "Rule/".
    rdbdir : str
        the path to "RDB/".

    do_ws : bool
        do word-segmentation.
    do_parse : bool
        do parsing.
    do_role : bool
        do role.

    sentence_delim: str
        the sentence delimiters.
    """

    # pylint: disable=invalid-name

    if ruledir is None:
        ruledir = _os.getenv('CKIPPARSER_RULE')
        if not ruledir:
            ruledir = _os.path.join(_sys.prefix, 'share', 'ckipnlp', 'Rule')
        if not _os.path.isdir(ruledir):
            _warnings.warn('Invalid ruledir (%s)' % ruledir)
            ruledir = 'Rule'

    if rdbdir is None:
        rdbdir = _os.getenv('CKIPPARSER_RDB')
        if not rdbdir:
            rdbdir = _os.path.join(_sys.prefix, 'share', 'ckipnlp', 'RDB')
        if not _os.path.isdir(rdbdir):
            _warnings.warn('Invalid rdbdir (%s)' % rdbdir)
            rdbdir = 'RDB'

    IsTag = not do_ws
    AssignRole = do_role
    AssignRoleOnly = False

    if not do_parse:
        if not do_ws and not do_role:
            raise ValueError('Must select at least one task')
        if do_ws and not do_role:
            raise ValueError('Use ckipws.CkipWs for word-segmentation')
        if not do_ws and do_role:
            AssignRoleOnly = True
        if do_ws and do_role:
            raise ValueError('Invalid tasks')

    cfg = []

    cfg.append(';PyCkip {version}'.format(version=_about.__version__))
    cfg.append(';parser.ini')
    cfg.append(';Auto-generated {date}'.format(date=_datetime.datetime.now()))
    cfg.append('')

    cfg.append('[WordSeg]')
    cfg.append('ini={wsinifile}'.format(wsinifile=wsinifile))
    cfg.append('')

    cfg.append('[Parser]')
    cfg.append('SetPos13=0')
    cfg.append('13CateFile={ruledir}/13Cate.txt'.format(ruledir=ruledir))
    cfg.append('')

    cfg.append('SetMap=1')
    cfg.append('CatMapFile={ruledir}/CatMap.txt'.format(ruledir=ruledir))
    cfg.append('WordLib1={ruledir}/WordLib1.txt'.format(ruledir=ruledir))
    cfg.append('WordLib2={ruledir}/WordLib2.txt'.format(ruledir=ruledir))
    cfg.append('WordLib3={ruledir}/WordLib3.txt'.format(ruledir=ruledir))
    cfg.append('')

    cfg.append('GrammarRule={ruledir}/CKIP-Rule.txt'.format(ruledir=ruledir))
    cfg.append('HeadRule={ruledir}/CKIP-Head.txt'.format(ruledir=ruledir))
    cfg.append('')

    cfg.append('SetChangePos=1')
    cfg.append('SentenceDelimiter={SentenceDelimiter}'.format(SentenceDelimiter=sentence_delim))
    cfg.append('SetLength=15')
    cfg.append('NormalPos=1')
    cfg.append('NormalTree=1')
    cfg.append('IsTag={IsTag}'.format(IsTag=int(IsTag)))
    cfg.append('')

    cfg.append('[SRL]')
    cfg.append('DataPath={rdbdir}/'.format(rdbdir=rdbdir))
    cfg.append('AssignRole={AssignRole}'.format(AssignRole=int(AssignRole)))
    cfg.append('AssignRoleOnly={AssignRoleOnly}'.format(AssignRoleOnly=int(AssignRoleOnly)))

    return '\n'.join(cfg), options
