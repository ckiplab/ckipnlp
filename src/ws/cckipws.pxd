# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2018-2019'

cdef extern:

	ctypedef void* wordseg_t

	wordseg_t WordSeg_New()
	int WordSeg_InitData(wordseg_t obj, char *FileName);
	int WordSeg_ApplyFile(wordseg_t obj, char *input, char *output, char *uwfile);
	int WordSeg_ApplyList(wordseg_t obj, int length, const Py_UNICODE **inputList);
	int WordSeg_ApplyArticle(wordseg_t obj, int length, const Py_UNICODE **inputList);
	const Py_UNICODE* WordSeg_GetResultBegin(wordseg_t obj);
	const Py_UNICODE* WordSeg_GetResultNext(wordseg_t obj);
	const Py_UNICODE* WordSeg_GetUWBegin(wordseg_t obj);
	const Py_UNICODE* WordSeg_GetUWNext(wordseg_t obj);
	void WordSeg_EnableConsoleLogger(wordseg_t obj);
	void WordSeg_Destroy(wordseg_t obj);
