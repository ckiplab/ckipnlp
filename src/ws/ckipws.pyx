# -*- coding:utf-8 -*-
# cython: language_level=3

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

cimport src.ws.cckipws as cckipws
cimport cython
from libcpp.vector cimport vector

@cython.final
cdef class CkipWsCore:

    cdef cckipws.wordseg_t __obj

    def __cinit__(self):
        self.__obj = cckipws.WordSeg_New()

    def __dealloc__(self):
        if self.__obj is not NULL:
            cckipws.WordSeg_Destroy(self.__obj)

    def init_data(self, str inifile):
        ret = cckipws.WordSeg_InitData(self.__obj, inifile.encode())
        if not ret:
            raise IOError()

    def enable_logger(self):
        cckipws.WordSeg_EnableConsoleLogger(self.__obj)

    def apply_list(self, vector[const Py_UNICODE*] ilist):

        ret = cckipws.WordSeg_ApplyList(self.__obj, ilist.size(), ilist.data())
        assert ret is not None

        olist = []
        result = cckipws.WordSeg_GetResultBegin(self.__obj)
        while result is not NULL:
            olist.append(result.strip())
            result = cckipws.WordSeg_GetResultNext(self.__obj)

        return olist

    def apply_file(self, str ifile, str ofile, str uwfile):
        ret = cckipws.WordSeg_ApplyFile(self.__obj, ifile.encode(), ofile.encode(), uwfile.encode())
        assert ret is not None
