# -*- coding:utf-8 -*-
# cython: language_level=3

from __future__ import print_function

__author__    = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2018-2019'
include '../about.pyx'
include 'ini.pyx'
include '../ckipws/ini.pyx'

cimport ckipparser.cckipparser as cckipparser
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

cdef class CkipParser:
	"""The CKIP parser driver.

	Args:
		logger (bool):   enable logger.
		inifile (str):   the path to the INI file.
		wsinifile (str): the path to the INI file for CKIPWS.
		options:         the options (see :func:`create_ws_ini` and  :func:`create_parser_ini`).
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
			wsinidata, options = create_ws_ini(**options)
			fwsini.write(__from_unicode(wsinidata))
			fwsini.flush()

		if not inifile:
			fini = __tempfile.NamedTemporaryFile(mode='w')
			inifile = fini.name
			inidata, options = create_parser_ini(wsinifile=wsinifile, **options)
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

	def __call__(self, text, *, unicode=False):
		"""Parse a sentence.

		Args:
			text (str):     the input sentence.
			unicode (bool): use Unicode for of input/output encoding; otherwise use system encoding.

		Return:
			str:            the output sentence.
		"""
		return self.apply_list([text], unicode=unicode)[0]

	def apply_list(self, ilist, *, unicode=False):
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

	def apply_file(self, *, ifile, ofile):
		"""Parse a file.

		Args:
			ifile (str): the input file.
			ofile (str): the output file (will be overwritten).
		"""
		ifile  = __to_bytes(ifile)
		ofile  = __to_bytes(ofile)

		ret = cckipparser.CKIPCoreNLP_ApplyFile(self.__obj, ifile, ofile)
		assert ret is not None
