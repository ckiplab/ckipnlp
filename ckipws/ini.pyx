# -*- coding:utf-8 -*-
# cython: language_level=3

__author__    = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2018-2019'


def create_ws_ini(*, data2dir=None, lexfile=None, new_style_format=False, show_category=True, **options):
	"""Generate CKIP word segmentation config.

	Args:
		data2dir (str): the path to the folder "Data2/".
		lexfile (str):  the path to the user-defined lexicon file.

		new_style_format (bool): split sentences by newline characters ("\\n") rather than punctuations.
		show_category (bool):    show part-of-speech tags.
	"""
	if data2dir is None:
		data2dir = __os.getenv('CKIPWS_DATA2')
		if not data2dir:
			data2dir = __os.path.join(__sys.prefix, 'share', 'pyckip', 'Data2')
		if not __os.path.isdir(data2dir):
			print('Warning: invalid data2dir (%s)')
			data2dir = 'Data2'

	cfg = []

	cfg.append(';PyCkip {version}'.format(version=__version__))
	cfg.append(';ws.ini')
	cfg.append(';Auto-generated {date}'.format(date=__datetime.datetime.now()))
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
	if lexfile: cfg.append('TextLexiconName=TextLex')
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
	if lexfile: cfg.append('TextLexiconName=TextLex')
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
	if lexfile: cfg.append('TextLexiconName=TextLex')
	cfg.append('CategoryPredictor=CatPred')
	cfg.append('InitDataPath={data2dir}/uwea/data/'.format(data2dir=data2dir))
	cfg.append('ApplyRule=639')
	cfg.append('')

	cfg.append('[CAffixCombiner]')
	cfg.append('Name=AC')
	cfg.append('LexiconName=Lex')
	if lexfile: cfg.append('TextLexiconName=TextLex')
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

	HandlerList = ['LWGen', 'myLWGen', 'DMMergedParser', 'RD3', 'RD6', 'RD7', 'FW', 'BW', 'MaxMatch', 'ProbModel', 'UW', \
			'DDMFPP', 'LWGen', 'UWGen', 'RWTBPP', 'LWGen', 'myLWGen', 'DMSplittedParser', 'BW', 'MaxMatch', 'ProbModel', 'CA']
	if not lexfile:
		while 'myLWGen' in HandlerList:
			HandlerList.remove('myLWGen')

	cfg.append('[CWordSegmentor]')
	cfg.append('Name=MainWS')
	cfg.append('ArticleMaxLineNum=300')
	cfg.append('SentenceMaxWordNum=80')
	cfg.append('ReloadMyDic=false')
	cfg.append('SentenceDelimiter=，,；。！？')
	cfg.append('HandlerList={HandlerList}'.format(HandlerList=' '.join(HandlerList)))
	cfg.append('Result=ProbModelResult')
	cfg.append('')

	return '\n'.join(cfg), options
