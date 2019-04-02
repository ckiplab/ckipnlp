# -*- coding:utf-8 -*-
# cython: language_level=3

from __future__ import print_function

__author__    = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2018-2019'
include '../about.pyx'

cimport ckipparser.cckipparser as cckipparser
from libc.stdlib cimport malloc, free
from cpython.unicode cimport PyUnicode_AsUnicode, PyUnicode_FromUnicode

import datetime as __datetime
import os       as __os
import re       as __re
import sys      as __sys
import tempfile as __tempfile

from ckipws import CkipWS as __CkipWS

def __to_bytes(text):
	return text.encode() if __sys.version_info >= (3, 0) else text

def __from_bytes(text):
	return text.decode() if __sys.version_info >= (3, 0) else text

def __to_unicode(text):
	return text if __sys.version_info >= (3, 0) else text.decode('utf-8')

def __from_unicode(text):
	return text if __sys.version_info >= (3, 0) else text.encode('utf-8')

cdef class CkipParser:
	"""The CKIP parser driver.

	Args:
		logger (bool): enable logger.
		inifile (str):   the INI file.
		wsinifile (str): the INI file for CKIPWS.
		options:         the optiones (see :func:`create_ini`).
	"""

	cdef cckipparser.corenlp_t __obj

	def __cinit__(self, *, logger=False, inifile=None, wsinifile=None, **options):

		self.__obj = cckipparser.CKIPCoreNLP_New()
		if self.__obj is NULL:
			raise MemoryError()

		if logger:
			self.enable_logger()

		if not wsinifile:
			fwsini = __tempfile.NamedTemporaryFile(mode='w')
			wsinifile = fwsini.name
			wsinidata, options = __CkipWS.create_ini(**options)
			fwsini.write(__from_unicode(wsinidata))
			fwsini.flush()

		if not inifile:
			fini = __tempfile.NamedTemporaryFile(mode='w')
			inifile = fini.name
			inidata, options = self.create_ini(wsinifile=wsinifile, **options)
			fini.write(__from_unicode(inidata))
			fini.flush()

		def CkipParser(*, _=None): return None
		CkipParser(**options)

		name = __to_bytes(inifile)
		ret = cckipparser.CKIPCoreNLP_InitData(self.__obj, name)
		if not ret:
			raise IOError()

		try:
			fwsini.close()
		except:
			pass

		try:
			fini.close()
		except:
			pass

	def __dealloc__(self):
		if self.__obj is not NULL:
			cckipparser.CKIPCoreNLP_Destroy(self.__obj)
			pass

	def enable_logger(self):
		"""Enable logger."""
		# cckipparser.CKIPCoreNLP_EnableConsoleLogger(self.__obj)
		pass

	def __call__(self, text, unicode=False):
		"""Parse a sentence.

		Args:
			text (str):     the input sentence.
			unicode (bool): use Unicode for of input/output encoding; otherwise use system encoding.

		Return:
			str:            the output sentence.
		"""
		return self.apply_list([text], unicode=unicode)[0]

	def apply_list(self, ilist, unicode=False):
		"""Parse a list of sentence.

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
		ret = cckipparser.CKIPCoreNLP_ApplyList(self.__obj, inum, iarr)
		free(iarr)
		assert ret is not None

		cdef const Py_UNICODE* result
		olist = []
		result = cckipparser.CKIPCoreNLP_GetResultBegin(self.__obj)
		while result is not NULL:
			olist.append(PyUnicode_FromUnicode(result, len(result)).strip())
			result = cckipparser.CKIPCoreNLP_GetResultNext(self.__obj)

		if not unicode:
			olist = [__from_unicode(l) for l in olist]

		return olist

	def apply_file(self, ifile=None, ofile=None):
		"""Parse a file.

		Args:
			ifile (str): the input file.
			ofile (str): the output file (will be overwritten).
		"""
		assert ifile is not None
		assert ofile is not None
		ifile  = __to_bytes(ifile)
		ofile  = __to_bytes(ofile)

		ret = cckipparser.CKIPCoreNLP_ApplyFile(self.__obj, ifile, ofile)
		assert ret is not None

	@staticmethod
	def create_ini(*, wsinifile=None, ruledir=None, rdbdir=None, \
			do_ws=True, do_parse=True, do_role=True, **options):
		"""Generate config.

		Args:
			ruledir (str): the path to "Rule/".
			rdbdir (str):  the path to "RDB/".

			do_ws (bool):    do word-segmentation.
			do_parse (bool): do parsing.
			do_role (bool):  do role.
		"""
		assert wsinifile is not None

		if ruledir is None:
			ruledir = __os.getenv('CKIPPARSER_RULE')
			if not ruledir:
				print('Warning: $CKIPPARSER_RULE is unset or null')

		if rdbdir is None:
			rdbdir = __os.getenv('CKIPPARSER_RDB')
			if not rdbdir:
				print('Warning: $CKIPPARSER_RDB is unset or null')

		IsTag          = not do_ws
		AssignRole     = do_role
		AssignRoleOnly = False

		if not do_parse:
			if not do_ws and not do_role:
				raise ValueError('Must select at least one task')
			if do_ws and not do_role:
				raise ValueError('Use ckipws.CkipWS for word-segmentation')
			if not do_ws and do_role:
				AssignRoleOnly = True
			if do_ws and do_role:
				raise ValueError('Invalid tasks')

		cfg = []

		cfg.append('[WordSeg]')
		cfg.append('ini={wsinifile}'.format(wsinifile=wsinifile))
		cfg.append('')

		cfg.append('[Parser]')
		cfg.append('SetPos13=0')
		cfg.append('13CateFile={ruledir}/13Cate.txt'.format(ruledir=ruledir))
		cfg.append('')

		# cfg.append('SetMap=1')
		cfg.append('SetMap=0')
		cfg.append('CatMapFile={ruledir}/CatMap.txt'.format(ruledir=ruledir))
		cfg.append('')

		cfg.append('GrammarRule={ruledir}/CKIP-Rule.txt'.format(ruledir=ruledir))
		cfg.append('HeadRule={ruledir}/CKIP-Head.txt'.format(ruledir=ruledir))
		cfg.append('')

		cfg.append('SetChangePos=1')
		cfg.append('SentenceDelimiter=，,；。！？')
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
