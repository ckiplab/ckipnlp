# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

cdef extern:

  ctypedef void* wordseg_t

  wordseg_t WordSeg_New() nogil;
  int WordSeg_InitData(wordseg_t obj, char *FileName) nogil;
  int WordSeg_ApplyFile(wordseg_t obj, char *input, char *output, char *uwfile) nogil;
  int WordSeg_ApplyList(wordseg_t obj, int length, const Py_UNICODE **inputList) nogil;
  int WordSeg_ApplyArticle(wordseg_t obj, int length, const Py_UNICODE **inputList) nogil;
  const Py_UNICODE* WordSeg_GetResultBegin(wordseg_t obj) nogil;
  const Py_UNICODE* WordSeg_GetResultNext(wordseg_t obj) nogil;
  const Py_UNICODE* WordSeg_GetUWBegin(wordseg_t obj) nogil;
  const Py_UNICODE* WordSeg_GetUWNext(wordseg_t obj) nogil;
  void WordSeg_EnableConsoleLogger(wordseg_t obj) nogil;
  void WordSeg_Destroy(wordseg_t obj) nogil;
