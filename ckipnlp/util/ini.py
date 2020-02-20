#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

import datetime as _datetime
import os as _os
import sys as _sys
import tempfile as _tempfile
import warnings as _warnings

import ckipnlp as _about

def create_ws_lex(*lex_list
):
    """Generate CKIP word segmentation lexicon file.

    Parameters
    ----------
        *lex_list : Tuple[str, str]
            the lexicon word and its POS-tag.

    Returns
    -------
        lex_file : str
            the name of the lexicon file.
        f_lex : TextIO
            the file object.

    .. attention::
        Remember to close **f_lex** manually.
    """

    f_lex = _tempfile.NamedTemporaryFile(mode='w')
    lex_file = f_lex.name

    for lex in lex_list:
        print('\t'.join(lex), file=f_lex)

    f_lex.flush()
    return lex_file, f_lex

def create_ws_ini(*, # pylint: disable=too-many-statements
    data2_dir=None,
    lex_file=None,
    new_style_format=False,
    show_category=True,
    sentence_max_word_num=80,
    **options,
):
    """Generate CKIP word segmentation config.

    Parameters
    ----------
        data2_dir : str
            the path to the folder "Data2/".
        lex_file : str
            the path to the user-defined lexicon file.

        new_style_format : bool
            split sentences by newline characters ("\\\\n") rather than punctuations.
        show_category : bool
            show part-of-speech tags.

        sentence_max_word_num : int
            maximum number of words per sentence.

    Returns
    -------
        ini_file : str
            the name of the config file.
        f_ini : TextIO
            the file object.

    .. attention::
        Remember to close **f_ini** manually.
    """

    # pylint: disable=invalid-name

    f_ini = _tempfile.NamedTemporaryFile(mode='w')
    ini_file = f_ini.name

    if data2_dir is None:
        data2_dir = _os.getenv('CKIPWS_DATA2')
        if not data2_dir:
            data2_dir = _os.path.join(_sys.prefix, 'share', 'ckipnlp', 'Data2')
        if not _os.path.isdir(data2_dir):
            _warnings.warn('Invalid data2_dir (%s)' % data2_dir)
            data2_dir = 'Data2'

    print(';PyCkip {version}'.format(version=_about.__version__), file=f_ini)
    print(';ws.ini', file=f_ini)
    print(';Auto-generated {date}'.format(date=_datetime.datetime.now()), file=f_ini)
    print('', file=f_ini)

    print('[ConsoleLogger]', file=f_ini)
    print('Name=ConsoleLogger', file=f_ini)
    print('', file=f_ini)

    if lex_file:
        print('[CTextLexicon]', file=f_ini)
        print('Name=TextLex', file=f_ini)
        print('FileName={lex_file}'.format(lex_file=lex_file), file=f_ini)
        print('', file=f_ini)

    print('[CLexicon]', file=f_ini)
    print('Name=Lex', file=f_ini)
    print('FileName={data2_dir}/Lexicon.Dat'.format(data2_dir=data2_dir), file=f_ini)
    print('', file=f_ini)

    print('[CALexicon]', file=f_ini)
    print('Name=CALex', file=f_ini)
    print('FileName={data2_dir}/CALexicon.Dat'.format(data2_dir=data2_dir), file=f_ini)
    print('', file=f_ini)

    print('[CDMMergedParser]', file=f_ini)
    print('Name=DMMergedParser', file=f_ini)
    print('GenerateMaxLengthWordOnly=no', file=f_ini)
    print('LexiconName=Lex', file=f_ini)
    print('', file=f_ini)

    print('[CDMSplittedParser]', file=f_ini)
    print('Name=DMSplittedParser', file=f_ini)
    print('GenerateMaxLengthWordOnly=no', file=f_ini)
    print('LexiconName=Lex', file=f_ini)
    print('', file=f_ini)

    print('[CHTRDRule3]', file=f_ini)
    print('Name=RD3', file=f_ini)
    print('LexiconName=Lex', file=f_ini)
    print('', file=f_ini)

    print('[CHTRDRule6]', file=f_ini)
    print('Name=RD6', file=f_ini)
    print('LexiconName=Lex', file=f_ini)
    print('', file=f_ini)

    print('[CHTRDRule7]', file=f_ini)
    print('Name=RD7', file=f_ini)
    print('LexiconName=Lex', file=f_ini)
    print('', file=f_ini)

    print('[CHTForeignWord]', file=f_ini)
    print('Name=FW', file=f_ini)
    print('LexiconName=Lex', file=f_ini)
    print('', file=f_ini)

    print('[CHTBoundWord]', file=f_ini)
    print('Name=BW', file=f_ini)
    print('LexiconName=Lex', file=f_ini)
    print('', file=f_ini)

    print('[CMaxMatch]', file=f_ini)
    print('Name=MaxMatch', file=f_ini)
    print('WindowSize=3', file=f_ini)
    print('', file=f_ini)

    print('[CHTCategoryPredictor]', file=f_ini)
    print('Name=CatPred', file=f_ini)
    print('PrefixCategoryFileName={data2_dir}/CatPredictData/PrefixCategoryFreq'.format(data2_dir=data2_dir), file=f_ini)
    print('PrefixFileName={data2_dir}/CatPredictData/PrefixFreq'.format(data2_dir=data2_dir), file=f_ini)
    print('SuffixCategoryFileName={data2_dir}/CatPredictData/SuffixCategoryFreq'.format(data2_dir=data2_dir), file=f_ini)
    print('SuffixFileName={data2_dir}/CatPredictData/SuffixFreq'.format(data2_dir=data2_dir), file=f_ini)
    print('', file=f_ini)

    print('[CStatProb]', file=f_ini)
    print('Name=CAProb1', file=f_ini)
    print('FileName={data2_dir}/CAStat-w(0)c(0)-w(-1).dat'.format(data2_dir=data2_dir), file=f_ini)
    print('', file=f_ini)

    print('[CStatProb]', file=f_ini)
    print('Name=CAProb2', file=f_ini)
    print('FileName={data2_dir}/CAStat-w(0)c(0)-w(1).dat'.format(data2_dir=data2_dir), file=f_ini)
    print('', file=f_ini)

    print('[CStatProb]', file=f_ini)
    print('Name=CAProb3', file=f_ini)
    print('FileName={data2_dir}/CAStat-w(0)c(0)-w(-2).dat'.format(data2_dir=data2_dir), file=f_ini)
    print('', file=f_ini)

    print('[CStatProb]', file=f_ini)
    print('Name=CAProb4', file=f_ini)
    print('FileName={data2_dir}/CAStat-w(0)c(0)-w(2).dat'.format(data2_dir=data2_dir), file=f_ini)
    print('', file=f_ini)

    print('[CoveringAmbiguity]', file=f_ini)
    print('Name=CA', file=f_ini)
    print('LexiconName=Lex', file=f_ini)
    print('CoveringAmbiguityLexiconName=CALex', file=f_ini)
    print('InsertSplittedWordsOnly=false', file=f_ini)
    print('StatisticProbability1=CAProb1', file=f_ini)
    print('StatisticProbability2=CAProb2', file=f_ini)
    print('StatisticProbability3=CAProb3', file=f_ini)
    print('StatisticProbability4=CAProb4', file=f_ini)
    print('', file=f_ini)

    print('[CStatProb]', file=f_ini)
    print('Name=Prob1', file=f_ini)
    print('FileName={data2_dir}/CKIPWStatistic-w(-1)-w(0).dat'.format(data2_dir=data2_dir), file=f_ini)
    print('', file=f_ini)

    print('[CStatProb]', file=f_ini)
    print('Name=Prob2', file=f_ini)
    print('FileName={data2_dir}/CKIPWStatistic-c(-1)-c(0).dat'.format(data2_dir=data2_dir), file=f_ini)
    print('', file=f_ini)

    print('[CStatProb]', file=f_ini)
    print('Name=Prob3', file=f_ini)
    print('FileName={data2_dir}/CKIPWStatistic-c(0)-w(0).dat'.format(data2_dir=data2_dir), file=f_ini)
    print('', file=f_ini)

    print('[CSimpleProbModel]', file=f_ini)
    print('Name=ProbModel', file=f_ini)
    print('StatisticProbability1=Prob1', file=f_ini)
    print('StatisticProbability2=Prob2', file=f_ini)
    print('StatisticProbability3=Prob3', file=f_ini)
    print('LexiconName=Lex', file=f_ini)
    if lex_file:
        print('TextLexiconName=TextLex', file=f_ini)
    print('AdjustProb3=true', file=f_ini)
    print('CoveringAmbiguityLexiconName=CALex', file=f_ini)
    print('CategoryPredictor=CatPred', file=f_ini)
    print('KeepBestCategory=true', file=f_ini)
    print('SimplifiedCategory=false', file=f_ini)
    print('', file=f_ini)

    print('[CDetectMonosyllabicMorpheme]', file=f_ini)
    print('Name=DMM', file=f_ini)
    print('ApplyDefaultHeuristicDetectRule=yes', file=f_ini)
    print('InitDataPath={data2_dir}/uwea/qrulepool/'.format(data2_dir=data2_dir), file=f_ini)
    print('', file=f_ini)

    print('[ChineseName]', file=f_ini)
    print('Name=CN', file=f_ini)
    print('LexiconName=Lex', file=f_ini)
    print('InitDataPath={data2_dir}/uwea/data/'.format(data2_dir=data2_dir), file=f_ini)
    print('', file=f_ini)

    print('[CForeignName]', file=f_ini)
    print('Name=FN', file=f_ini)
    print('LexiconName=Lex', file=f_ini)
    if lex_file:
        print('TextLexiconName=TextLex', file=f_ini)
    print('InitDataPath={data2_dir}/uwea/data/'.format(data2_dir=data2_dir), file=f_ini)
    print('', file=f_ini)

    print('[CompoundWord]', file=f_ini)
    print('Name=CW', file=f_ini)
    print('LexiconName=Lex', file=f_ini)
    print('InitDataPath={data2_dir}/uwea/data/'.format(data2_dir=data2_dir), file=f_ini)
    print('', file=f_ini)

    print('[CStatisticWord]', file=f_ini)
    print('Name=SW', file=f_ini)
    print('LexiconName=Lex', file=f_ini)
    if lex_file:
        print('TextLexiconName=TextLex', file=f_ini)
    print('CategoryPredictor=CatPred', file=f_ini)
    print('InitDataPath={data2_dir}/uwea/data/'.format(data2_dir=data2_dir), file=f_ini)
    print('ApplyRule=639', file=f_ini)
    print('', file=f_ini)

    print('[CAffixCombiner]', file=f_ini)
    print('Name=AC', file=f_ini)
    print('LexiconName=Lex', file=f_ini)
    if lex_file:
        print('TextLexiconName=TextLex', file=f_ini)
    print('CategoryPredictor=CatPred', file=f_ini)
    print('', file=f_ini)

    print('[CSimilarStructureCombiner]', file=f_ini)
    print('Name=SSC', file=f_ini)
    print('AutoCombineWordLen=2', file=f_ini)
    print('HeuristicCombinedWordMaxLen=3', file=f_ini)
    print('LexiconName=Lex', file=f_ini)
    print('CategoryPredictor=CatPred', file=f_ini)
    print('', file=f_ini)

    print('[COnlineLexicon]', file=f_ini)
    print('Name=OnlineLexForUWGen', file=f_ini)
    print('', file=f_ini)

    print('[CUnknownWord]', file=f_ini)
    print('Name=UW', file=f_ini)
    print('UnknownWordGeneratorList=DMM CN FN CW SW SSC', file=f_ini)
    print('OnlineLexicon=OnlineLexForUWGen', file=f_ini)
    print('', file=f_ini)

    if lex_file:
        print('[CLexWordGenerator]', file=f_ini)
        print('Name=myLWGen', file=f_ini)
        print('LexiconName=TextLex', file=f_ini)
        print('', file=f_ini)

    print('[CLexWordGenerator]', file=f_ini)
    print('Name=LWGen', file=f_ini)
    print('LexiconName=Lex', file=f_ini)
    print('', file=f_ini)

    print('[CLexWordGenerator]', file=f_ini)
    print('Name=LWGen1', file=f_ini)
    print('LexiconName=Lex', file=f_ini)
    print('MaxWordLen=1', file=f_ini)
    print('', file=f_ini)

    print('[CLexWordGenerator]', file=f_ini)
    print('Name=UWGen', file=f_ini)
    print('LexiconName=OnlineLexForUWGen', file=f_ini)
    print('', file=f_ini)

    print('[CSimpleProbModelResult]', file=f_ini)
    print('Name=ProbModelResult', file=f_ini)
    print('ProbabilityModelName=ProbModel', file=f_ini)
    print('NewStyleFormat={NewStyleFormat}'.format(NewStyleFormat=str(new_style_format).lower()), file=f_ini)
    print('ShowCategory={ShowCategory}'.format(ShowCategory=str(show_category).lower()), file=f_ini)
    print('LexiconName=Lex', file=f_ini)
    print('CategoryPredictor=CatPred', file=f_ini)
    print('KeepExistingWord=true', file=f_ini)
    print('FeatureAssigner=FA', file=f_ini)
    print('FilterBadWord=false', file=f_ini)
    print('', file=f_ini)

    print('[CDetectDMForPostProcess]', file=f_ini)
    print('Name=DDMFPP', file=f_ini)
    print('', file=f_ini)

    print('[CRemoveWordToBePostProcessed]', file=f_ini)
    print('Name=RWTBPP', file=f_ini)
    print('', file=f_ini)

    handler_list = [
        'LWGen', 'myLWGen', 'DMMergedParser', 'RD3', 'RD6', 'RD7', 'FW', 'BW', 'MaxMatch', 'ProbModel', 'UW', 'DDMFPP',
        'LWGen', 'UWGen', 'RWTBPP', 'LWGen', 'myLWGen', 'DMSplittedParser', 'BW', 'MaxMatch', 'ProbModel', 'CA'
    ]

    if not lex_file:
        while 'myLWGen' in handler_list:
            handler_list.remove('myLWGen')

    print('[CWordSegmentor]', file=f_ini)
    print('Name=MainWS', file=f_ini)
    print('ArticleMaxLineNum=300', file=f_ini)
    print('SentenceMaxWordNum={sentence_max_word_num}'.format(sentence_max_word_num=sentence_max_word_num), file=f_ini)
    print('ReloadMyDic=false', file=f_ini)
    print('SentenceDelimiter=，,；。！？', file=f_ini)
    print('HandlerList={handler_list}'.format(handler_list=' '.join(handler_list)), file=f_ini)
    print('Result=ProbModelResult', file=f_ini)
    print('', file=f_ini)

    f_ini.flush()
    return ini_file, f_ini, options

def create_parser_ini(*, # pylint: disable=too-many-statements
    ws_ini_file,
    rule_dir=None,
    rdb_dir=None,
    do_ws=True,
    do_parse=True,
    do_role=True,
    sentence_delim='，,；。！？',
    **options,
):
    """Generate CKIP parser config.

    Parameters
    ----------
        rule_dir : str
            the path to "Rule/".
        rdb_dir : str
            the path to "RDB/".

        do_ws : bool
            do word-segmentation.
        do_parse : bool
            do parsing.
        do_role : bool
            do role.

        sentence_delim : str
            the sentence delimiters.

    Returns
    -------
        ini_file : str
            the name of the config file.
        f_ini : TextIO
            the file object.

    .. attention::
        Remember to close **f_ini** manually.
    """

    # pylint: disable=invalid-name

    f_ini = _tempfile.NamedTemporaryFile(mode='w')
    ini_file = f_ini.name

    if rule_dir is None:
        rule_dir = _os.getenv('CKIPPARSER_RULE')
        if not rule_dir:
            rule_dir = _os.path.join(_sys.prefix, 'share', 'ckipnlp', 'Rule')
        if not _os.path.isdir(rule_dir):
            _warnings.warn('Invalid rule_dir (%s)' % rule_dir)
            rule_dir = 'Rule'

    if rdb_dir is None:
        rdb_dir = _os.getenv('CKIPPARSER_RDB')
        if not rdb_dir:
            rdb_dir = _os.path.join(_sys.prefix, 'share', 'ckipnlp', 'RDB')
        if not _os.path.isdir(rdb_dir):
            _warnings.warn('Invalid rdb_dir (%s)' % rdb_dir)
            rdb_dir = 'RDB'

    is_tag = not do_ws
    assign_role = do_role
    assign_role_only = False

    if not do_parse:
        if not do_ws and not do_role:
            raise ValueError('Must select at least one task')
        if do_ws and not do_role:
            raise ValueError('Use ckipws.CkipWs for word-segmentation')
        if not do_ws and do_role:
            assign_role_only = True
        if do_ws and do_role:
            raise ValueError('Invalid tasks')

    print(';PyCkip {version}'.format(version=_about.__version__), file=f_ini)
    print(';parser.ini', file=f_ini)
    print(';Auto-generated {date}'.format(date=_datetime.datetime.now()), file=f_ini)
    print('', file=f_ini)

    print('[WordSeg]', file=f_ini)
    print('ini={ws_ini_file}'.format(ws_ini_file=ws_ini_file), file=f_ini)
    print('', file=f_ini)

    print('[Parser]', file=f_ini)
    print('SetPos13=0', file=f_ini)
    print('13CateFile={rule_dir}/13Cate.txt'.format(rule_dir=rule_dir), file=f_ini)
    print('', file=f_ini)

    print('SetMap=1', file=f_ini)
    print('CatMapFile={rule_dir}/CatMap.txt'.format(rule_dir=rule_dir), file=f_ini)
    print('WordLib1={rule_dir}/WordLib1.txt'.format(rule_dir=rule_dir), file=f_ini)
    print('WordLib2={rule_dir}/WordLib2.txt'.format(rule_dir=rule_dir), file=f_ini)
    print('WordLib3={rule_dir}/WordLib3.txt'.format(rule_dir=rule_dir), file=f_ini)
    print('', file=f_ini)

    print('GrammarRule={rule_dir}/CKIP-Rule.txt'.format(rule_dir=rule_dir), file=f_ini)
    print('HeadRule={rule_dir}/CKIP-Head.txt'.format(rule_dir=rule_dir), file=f_ini)
    print('', file=f_ini)

    print('SetChangePos=1', file=f_ini)
    print('SentenceDelimiter={SentenceDelimiter}'.format(SentenceDelimiter=sentence_delim), file=f_ini)
    print('SetLength=15', file=f_ini)
    print('NormalPos=1', file=f_ini)
    print('NormalTree=1', file=f_ini)
    print('IsTag={is_tag}'.format(is_tag=int(is_tag)), file=f_ini)
    print('', file=f_ini)

    print('[SRL]', file=f_ini)
    print('DataPath={rdb_dir}/'.format(rdb_dir=rdb_dir), file=f_ini)
    print('AssignRole={assign_role}'.format(assign_role=int(assign_role)), file=f_ini)
    print('AssignRoleOnly={assign_role_only}'.format(assign_role_only=int(assign_role_only)), file=f_ini)

    f_ini.flush()
    return ini_file, f_ini, options
