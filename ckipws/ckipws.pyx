# -*- coding:utf-8 -*-
# cython: language_level=3

from __future__ import print_function

__author__    = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2018-2019'
include '../about.pyx'

cimport ckipws.cckipws as cckipws
from libc.stdlib cimport malloc, free
from cpython.unicode cimport PyUnicode_AsUnicode, PyUnicode_FromUnicode

import datetime as __datetime
import os       as __os
import re       as __re
import sys      as __sys
import tempfile as __tempfile

def __to_bytes(text):
	return text.encode() if __sys.version_info >= (3, 0) else text

def __from_bytes(text):
	return text.decode() if __sys.version_info >= (3, 0) else text

def __to_unicode(text):
	return text if __sys.version_info >= (3, 0) else text.decode('utf-8')

def __from_unicode(text):
	return text if __sys.version_info >= (3, 0) else text.encode('utf-8')

cdef class CkipWS:
	"""The CKIP word segmentation driver.

	Args:
		logger (bool): enable logger.
		inifile (str): the path to the INI file.
		options:       the options (see :func:`create_ini`).
	"""

	cdef cckipws.wordseg_t __obj

	def __cinit__(self, *, logger=False, inifile=None, **options):

		self.__obj = cckipws.WordSeg_New()
		if self.__obj is NULL:
			raise MemoryError()

		if logger:
			self.enable_logger()

		if not inifile:
			fini = __tempfile.NamedTemporaryFile(mode='w')
			inifile = fini.name
			inidata, options = self.create_ini(**options)
			fini.write(__from_unicode(inidata))
			fini.flush()

		def CkipWS(*, _=None): return None
		CkipWS(**options)

		name = __to_bytes(inifile)
		ret = cckipws.WordSeg_InitData(self.__obj, name)
		if not ret:
			raise IOError()

		try:
			fini.close()
		except:
			pass

	def __dealloc__(self):
		if self.__obj is not NULL:
			cckipws.WordSeg_Destroy(self.__obj)
			pass

	def enable_logger(self):
		"""Enable logger."""
		cckipws.WordSeg_EnableConsoleLogger(self.__obj)

	def __call__(self, text, unicode=False):
		"""Segment a sentence.

		Args:
			text (str):     the input sentence.
			unicode (bool): use Unicode for of input/output encoding; otherwise use system encoding.

		Return:
			str:            the output sentence.
		"""
		return self.apply_list([text], unicode=unicode)[0]

	def apply_list(self, ilist, unicode=False):
		"""Segment a list of sentence.

		Args:
			ilist (list):   the list of input sentences (str).
			unicode (bool): use Unicode for of input/output encoding; otherwise use system encoding.

		Return:
			list:           the list of output sentences (str).
		"""

		inum = len(ilist)
		if not unicode:
			ilist = [__to_unicode(l) for l in ilist]

		iarr = <const Py_UNICODE**> malloc(sizeof(const Py_UNICODE*) * inum)
		for i in range(inum):
			iarr[i] = PyUnicode_AsUnicode(ilist[i])
		ret = cckipws.WordSeg_ApplyList(self.__obj, inum, iarr)
		free(iarr)
		assert ret is not None

		cdef const Py_UNICODE* result
		olist = []
		result = cckipws.WordSeg_GetResultBegin(self.__obj)
		while result is not NULL:
			olist.append(PyUnicode_FromUnicode(result, len(result)).strip())
			result = cckipws.WordSeg_GetResultNext(self.__obj)

		if not unicode:
			olist = [__from_unicode(l) for l in olist]

		return olist

	def apply_file(self, ifile=None, ofile=None, uwfile=''):
		"""Segment a file.

		Args:
			ifile (str):  the input file.
			ofile (str):  the output file (will be overwritten).
			uwfile (str): the unknown word file (will be overwritten).
		"""
		assert ifile is not None
		assert ofile is not None
		ifile  = __to_bytes(ifile)
		ofile  = __to_bytes(ofile)
		uwfile = __to_bytes(uwfile)

		ret = cckipws.WordSeg_ApplyFile(self.__obj, ifile, ofile, uwfile)
		assert ret is not None

	@staticmethod
	def create_ini(*, data2dir=None, lexfile=None, new_style_format=False, show_category=True, **options):
		"""Generate config.

		Args:
			data2dir (str): the path to the folder "Data2/".
			lexfile (str):  the path to the user-defined lexicon file.

			new_style_format (bool): split sentences by newline characters ("\\n") rather than punctuations.
			show_category (bool):    show part-of-speech tags.
		"""
		if data2dir is None:
			data2dir = __os.getenv('CKIPWS_DATA2')
			if not data2dir:
				print('Warning: $CKIPWS_DATA2 is unset or null')

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
		if lexfile: print('TextLexiconName=TextLex')
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
		if lexfile: print('TextLexiconName=TextLex')
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
		if lexfile: print('TextLexiconName=TextLex')
		cfg.append('CategoryPredictor=CatPred')
		cfg.append('InitDataPath={data2dir}/uwea/data/'.format(data2dir=data2dir))
		cfg.append('ApplyRule=639')
		cfg.append('')

		cfg.append('[CAffixCombiner]')
		cfg.append('Name=AC')
		cfg.append('LexiconName=Lex')
		if lexfile: print('TextLexiconName=TextLex')
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

		HandlerList = ['LWGen', 'myLWGen', 'DMMergedParser', 'RD3', 'RD6', 'RD7', 'FW', 'BW', 'MaxMatch', 'ProbModel', 'UW', 'DDMFPP', 'LWGen', 'UWGen', 'RWTBPP', 'LWGen', 'myLWGen', 'DMSplittedParser', 'BW', 'MaxMatch', 'ProbModel', 'CA']
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
