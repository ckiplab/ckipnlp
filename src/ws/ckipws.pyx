# -*- coding:utf-8 -*-
# cython: language_level=3

__author__ = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2018-2019'

cimport src.ws.cckipws as cckipws
from libc.stdlib cimport malloc, free
from cpython.unicode cimport PyUnicode_AsUnicode

cdef class CkipWsCore:

    cdef cckipws.wordseg_t __obj

    def __cinit__(self):
        self.__obj = cckipws.WordSeg_New()

    def __dealloc__(self):
        if self.__obj is not NULL:
            cckipws.WordSeg_Destroy(self.__obj)
            pass

    def init_data(self, inifile):
        ret = cckipws.WordSeg_InitData(self.__obj, inifile.encode())
        if not ret:
            raise IOError()

    def enable_logger(self):
        cckipws.WordSeg_EnableConsoleLogger(self.__obj)

    def apply_list(self, ilist):
        inum = len(ilist)

        iarr = <const Py_UNICODE**> malloc(sizeof(const Py_UNICODE*) * inum)
        for i in range(inum):
            iarr[i] = PyUnicode_AsUnicode(ilist[i])
        ret = cckipws.WordSeg_ApplyList(self.__obj, inum, iarr)
        free(iarr)
        assert ret is not None

        olist = []
        result = cckipws.WordSeg_GetResultBegin(self.__obj)
        while result is not NULL:
            olist.append(result.strip())
            result = cckipws.WordSeg_GetResultNext(self.__obj)

        return olist

    def apply_file(self, ifile, ofile, uwfile):
        ret = cckipws.WordSeg_ApplyFile(self.__obj, ifile.encode(), ofile.encode(), uwfile.encode())
        assert ret is not None
