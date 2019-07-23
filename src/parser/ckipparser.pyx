# -*- coding:utf-8 -*-
# cython: language_level=3

__author__ = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2018-2019'

cimport src.parser.cckipparser as cckipparser
from libc.stdlib cimport malloc, free
from cpython.unicode cimport PyUnicode_AsUnicode

cdef class CkipParserCore:

    cdef cckipparser.corenlp_t __obj

    def __cinit__(self):
        self.__obj = cckipparser.CKIPCoreNLP_New()

    def __dealloc__(self):
        if self.__obj is not NULL:
            cckipparser.CKIPCoreNLP_Destroy(self.__obj)
            pass

    def init_data(self, inifile):
        ret = cckipparser.CKIPCoreNLP_InitData(self.__obj, inifile.encode())
        if not ret:
            raise IOError()

    def apply_list(self, ilist):
        inum = len(ilist)

        iarr = <const Py_UNICODE**> malloc(sizeof(const Py_UNICODE*) * inum)
        for i in range(inum):
            iarr[i] = PyUnicode_AsUnicode(ilist[i])
        ret = cckipparser.CKIPCoreNLP_ApplyList(self.__obj, inum, iarr)
        free(iarr)
        assert ret is not None

        olist = []
        result = cckipparser.CKIPCoreNLP_GetResultBegin(self.__obj)
        while result is not NULL:
            olist.append(result.strip())
            result = cckipparser.CKIPCoreNLP_GetResultNext(self.__obj)

        return olist

    def apply_file(self, ifile, ofile):
        ret = cckipparser.CKIPCoreNLP_ApplyFile(self.__obj, ifile.encode(), ofile.encode())
        assert ret is not None
