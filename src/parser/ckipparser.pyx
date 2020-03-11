# -*- coding:utf-8 -*-
# cython: language_level=3

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

cimport src.parser.cckipparser as cckipparser
cimport cython
from libcpp.vector cimport vector

@cython.final
cdef class CkipParserCore:

    cdef cckipparser.corenlp_t __obj

    def __cinit__(self):
        self.__obj = cckipparser.CKIPCoreNLP_New()

    def __dealloc__(self):
        if self.__obj is not NULL:
            cckipparser.CKIPCoreNLP_Destroy(self.__obj)

    def init_data(self, str inifile):
        ret = cckipparser.CKIPCoreNLP_InitData(self.__obj, inifile.encode())
        if not ret:
            raise IOError()

    # def enable_logger(self):
    #     cckipparser.CKIPCoreNLP_EnableConsoleLogger(self.__obj)

    def apply_list(self, vector[const Py_UNICODE*] ilist):

        ret = cckipparser.CKIPCoreNLP_ApplyList(self.__obj, ilist.size(), ilist.data())
        assert ret is not None

        cdef vector[const Py_UNICODE*] olist
        result = cckipparser.CKIPCoreNLP_GetResultBegin(self.__obj)
        while result is not NULL:
            olist.push_back(result)
            result = cckipparser.CKIPCoreNLP_GetResultNext(self.__obj)

        return olist

    def apply_file(self, str ifile, str ofile):
        ret = cckipparser.CKIPCoreNLP_ApplyFile(self.__obj, ifile.encode(), ofile.encode())
        assert ret is not None
