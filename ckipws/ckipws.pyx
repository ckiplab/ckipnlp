# -*- coding:utf-8 -*-
# cython: language_level=3

from __future__ import print_function

__author__    = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2018-2019'
include '../about.pyx'
include 'ini.pyx'

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
		options:       the options (see :func:`create_ws_ini`).
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
			inidata, options = create_ws_ini(**options)
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

	def __call__(self, text, *, unicode=False):
		"""Segment a sentence.

		Args:
			text (str):     the input sentence.
			unicode (bool): use Unicode for of input/output encoding; otherwise use system encoding.

		Return:
			str:            the output sentence.
		"""
		return self.apply_list([text], unicode=unicode)[0]

	def apply_list(self, ilist, *, unicode=False):
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

	def apply_file(self, *, ifile, ofile, uwfile=''):
		"""Segment a file.

		Args:
			ifile (str):  the input file.
			ofile (str):  the output file (will be overwritten).
			uwfile (str): the unknown word file (will be overwritten).
		"""
		ifile  = __to_bytes(ifile)
		ofile  = __to_bytes(ofile)
		uwfile = __to_bytes(uwfile)

		ret = cckipws.WordSeg_ApplyFile(self.__obj, ifile, ofile, uwfile)
		assert ret is not None
