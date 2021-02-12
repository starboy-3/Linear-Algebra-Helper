from sys import stdin
from copy import deepcopy


class MatrixError(Exception):
    def __init__(self, matrix1, matrix2):
        self.matrix1 = matrix1
        self.matrix2 = matrix2


class Matrix(object):
    def __init__(self, matrix):
        self.matrix = deepcopy(matrix)
        self.rows = len(matrix)
        self.columns = len(matrix[0])

    def __str__(self):
        out = ('\t'.join(map(str, row)) for row in self.matrix)
        return '\n'.join(out)

    def size(self):
        return (self.rows, self.columns)

    def __add__(self, other):
        if self.rows != other.rows or self.columns != other.columns:
            raise MatrixError(self, other)

        result = deepcopy(self)
        for i in range(self.rows):
            for j in range(self.columns):
                result.matrix[i][j] += other.matrix[i][j]
        return result

    def __mul__(self, other):
        if type(other) in [float, int]:
            multiplied = deepcopy(self)
            for i in range(self.rows):
                for j in range(self.columns):
                    multiplied.matrix[i][j] *= other
            return multiplied
        else:
            if self.columns != other.rows:
                raise MatrixError(self, other)

            C = [[0] * other.columns for _ in range(self.rows)]
            for i in range(self.rows):
                for j in range(other.columns):
                    for k in range(self.columns):
                        C[i][j] += self.matrix[i][k] * \
                                   other.matrix[k][j]
            return Matrix(C)

    def __rmul__(self, other):
        return self * other

    def transpose(self):
        values = [[0] * self.rows for _ in range(self.columns)]
        for i in range(self.rows):
            for j in range(self.columns):
                values[j][i] = self.matrix[i][j]
        self.matrix = values
        self.columns, self.rows = self.rows, self.columns
        return self

    @staticmethod
    def transposed(mat):
        values = [[0] * mat.rows for _ in range(mat.columns)]
        for i in range(mat.rows):
            for j in range(mat.columns):
                values[j][i] = mat.matrix[i][j]
        return Matrix(values)

    def __getitem__(self, item):
        return self.matrix[item]

    def solve(self, other):
        new = deepcopy(self.matrix)
        for i in range(self.rows):
            if new[i][i] == 0:
                raise MatrixError(self, self)
            for j in range(i + 1, self.columns):
                new[i][j] /= new[i][i]
            other[i] /= new[i][i]
            new[i][i] = 1.0
            for j in range(i + 1, self.rows):
                k = new[j][i]
                for t in range(i, self.columns):
                    new[j][t] -= new[i][t] * k
                other[j] -= other[i] * k
        for i in range(self.rows - 1, 0, -1):
            for j in range(i - 1, -1, -1):
                other[j] -= other[i] * new[j][i]
                new[j][i] = 0
        return other


class SquareMatrix(Matrix):
    def __pow__(self, power, modulo=None):
        ans = SquareMatrix([[0] * self.columns for _ in range(self.rows)])

        if power == 0:
            for i in range(self.columns):
                ans[i][i] = 1
            return ans

        if power % 2 == 0:
            ans = self ** (power // 2)
            return ans * ans

        ans = self ** (power - 1)
        return self * ans

    def __mul__(self, other):
        return super().__mul__(other)


exec(stdin.read())
