# !/usr/bin/env python
# -*- coding: utf-8 -*-
import baseObject
import funcUtil
import copy
import math

'''
    自己编写的矩阵运算的类
    （经过测试，该类的运行速度太慢，不建议使用；建议直接引用 numpy 进行矩阵运算，这样会快非常非常多）
'''
class Matrix(baseObject.base):
    def __init__(self, matrix=None):
        if matrix:
            self.load(matrix)
        else:
            self.__matrix = []
            self.__rowSize = 0
            self.__colSize = 0

    def load(self, list_2d):
        # self.__matrix = copy.deepcopy(list_2d)
        self.__matrix = list_2d
        self.__recalculateSize()

    def pointCalculate(self, matrix, func):
        matrix = self.__transformParam(matrix)
        row_size, col_size = self.getSizeFromList(matrix)
        tmp_matrix = self.get2dList()

        if row_size == self.__rowSize and col_size == self.__colSize:
            for i, vi in enumerate(matrix):
                for j, vj in enumerate(vi):
                    tmp_matrix[i][j] = func(tmp_matrix[i][j], vj)
        elif col_size == 1 and row_size == 1:
            for i, vi in enumerate(tmp_matrix):
                for j, vj in enumerate(vi):
                    tmp_matrix[i][j] = func(vj, matrix[0][0])
        elif row_size == self.__rowSize and (col_size == 1 or self.__colSize == 1):
            if col_size == 1:
                for i, vi in enumerate(tmp_matrix):
                    for j, vj in enumerate(vi):
                        tmp_matrix[i][j] = func(vj, matrix[i][0])
            elif self.__colSize == 1:
                for i, vi in enumerate(matrix):
                    for j, vj in enumerate(vi):
                        matrix[i][j] = func(tmp_matrix[i][0], vj)
                tmp_matrix = matrix
        elif col_size == self.__colSize and (row_size == 1 or self.__rowSize == 1):
            if row_size == 1:
                for i, vi in enumerate(tmp_matrix):
                    for j, vj in enumerate(vi):
                        tmp_matrix[i][j] = func(vj, matrix[0][i])
            elif self.__colSize == 1:
                for i, vi in enumerate(matrix):
                    for j, vj in enumerate(vi):
                        matrix[i][j] = func(tmp_matrix[0][j], vj)
                tmp_matrix = matrix
        else:
            return

        o_matrix = Matrix(tmp_matrix)
        # del tmp_matrix
        # del matrix
        return o_matrix

    def add(self, matrix):
        return self.pointCalculate(matrix, (lambda a, b: a + b))

    def minus(self, matrix):
        return self.pointCalculate(matrix, (lambda a, b: a - b))

    def pointMulti(self, matrix):
        return self.pointCalculate(matrix, (lambda a, b: a * b))

    def pointDivide(self, matrix):
        return self.pointCalculate(matrix, (lambda a, b: a / b))

    def multi(self, matrix):
        matrix = self.__transformParam(matrix)
        row_size, col_size = self.getSizeFromList(matrix)
        new_matrix = []

        for i, vi in enumerate(self.__matrix):
            row = []
            for k in range(col_size):
                _sum = 0
                for j in range(row_size):
                    _sum += vi[j] * matrix[j][k]
                row.append(_sum)
            new_matrix.append(row)

        o_matrix = Matrix(new_matrix)
        # del new_matrix
        return o_matrix

    def pow(self, times):
        tmp_matrix = self.get2dList()
        for i, vi in enumerate(tmp_matrix):
            for j, vj in enumerate(vi):
                tmp_matrix[i][j] = math.pow(vj, times)
        o_matrix = Matrix(tmp_matrix)
        # del tmp_matrix
        return o_matrix

    def sum(self):
        _sum = 0
        for i, vi in enumerate(self.__matrix):
            for j, vj in enumerate(vi):
                _sum += vj
        return _sum

    def transpose(self):
        matrix = []
        for j in range(self.__colSize):
            col = []
            for i in range(self.__rowSize):
                col.append(self.__matrix[i][j])
            matrix.append(col)
        self.__matrix = matrix
        self.__recalculateSize()
        return self

    def appendRow(self, matrix):
        matrix = self.__transformParam(matrix)

        for i in matrix:
            self.__matrix.append(i)
        self.__recalculateSize()
        # del matrix
        return self

    def prependRow(self, matrix):
        matrix = self.__transformParam(matrix)

        matrix.reverse()
        for i in matrix:
            self.__matrix.insert(0, i)
        self.__recalculateSize()
        # del matrix
        return self

    def appendCol(self, matrix):
        matrix = self.__transformParam(matrix)

        for i, v in enumerate(matrix):
            for j in v:
                self.__matrix[i].append(j)
        # del matrix
        return self

    def prependCol(self, matrix):
        matrix = self.__transformParam(matrix)

        for i, v in enumerate(matrix):
            # tmp_v = copy.copy(v)
            tmp_v = v
            tmp_v.reverse()
            for j in tmp_v:
                self.__matrix[i].insert(0, j)
        # del matrix
        return self

    def getMatrix(self, row_start=None, row_end=None, col_start=None, col_end=None):
        # tmp_matrix = copy.deepcopy(self.__matrix[row_start: row_end])
        tmp_matrix = self.__matrix[row_start: row_end]
        for i, v in enumerate(tmp_matrix):
            tmp_matrix[i] = v[col_start: col_end]
        o_matrix = Matrix(tmp_matrix)
        # del tmp_matrix
        return o_matrix

    def size(self):
        return self.__rowSize, self.__colSize

    def get2dList(self):
        # return copy.deepcopy(self.__matrix)
        return self.__matrix

    def __recalculateSize(self):
        self.__rowSize, self.__colSize = self.getSizeFromList(self.__matrix)

    def __transformParam(self, matrix):
        if isinstance(matrix, type(self)):
            return matrix.get2dList()
        elif isinstance(matrix, list):
            row_size, col_size = self.getSizeFromList(matrix)
            if col_size == 1:
                matrix = self.list1dTo2d(matrix)
            # return copy.deepcopy(matrix)
            return matrix
        elif isinstance(matrix, int) or isinstance(matrix, float) or isinstance(matrix, long):
            return [[matrix]]
        return

    @staticmethod
    def getSizeFromList(_list):
        if not isinstance(_list, list):
            return 1, 1

        col_size = 1
        if isinstance(_list[0], list):
            col_size = len(_list[0])
        return len(_list), col_size

    @staticmethod
    def list1dTo2d(list_1d):
        # list_2d = copy.deepcopy(list_1d)
        list_2d = list_1d
        for i, v in enumerate(list_2d):
            if isinstance(i, list):
                continue
            list_2d[i] = [v]
        return list_2d

    @staticmethod
    def ones(row_num, col_num):
        tmp_matrix = [[1 for j in range(col_num)] for i in range(row_num)]
        o_matrix = Matrix(tmp_matrix)
        # del tmp_matrix
        return o_matrix

    @staticmethod
    def zeros(row_num, col_num):
        tmp_matrix = [[0 for j in range(col_num)] for i in range(row_num)]
        o_matrix = Matrix(tmp_matrix)
        # del tmp_matrix
        return o_matrix
