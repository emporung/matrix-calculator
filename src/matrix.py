import math
class Matrix:
    def __init__(self, data):
        if not data or not all(isinstance(row, list) for row in data):
            raise ValueError("Матрица должна быть непустым списком списков")
        if len(set(len(row) for row in data)) != 1:
            raise ValueError("Строки матрицы должны быть одинаковх размеров")
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])
    
    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Сложение определено только для матриц одинаковых размеров")
        result = []
        for i in range(self.rows):          
            row = []
            for j in range(self.cols):      
                element = self.data[i][j] + other.data[i][j]
                row.append(element)
            result.append(row) 
        return Matrix(result)
    def __sub__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Вычитание определено только для матриц одинаковых размеров")
        result = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                element = self.data[i][j] - other.data[i][j]
                row.append(element)
            result.append(row)
        return Matrix(result)
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            result = []
            for i in range(self.rows):
                row = []
                for j in range(self.cols):
                    row.append(self.data[i][j] * other)
                result.append(row)
            return Matrix(result)
        else:
            if self.cols != other.rows:
                raise ValueError(f"Нльзя умножить матрицы таких размеров: {self.cols} столбцов != {other.rows} строк")
            result = []
            for i in range(self.rows):
                row = []
                for j in range(other.cols):
                    summa = 0
                    for k in range(self.cols):
                        summa += self.data[i][k] * other.data[k][j]
                    row.append(summa)
                result.append(row)
            return Matrix(result)
    def is_square(self):
        return self.rows == self.cols    
    def transpose(self):
        result = []
        for j in range(self.cols):
            row = []
            for i in range(self.rows):
                row.append(self.data[i][j])
            result.append(row)    
        return Matrix(result)
    def determinant(self):
        if not self.is_square():
            raise ValueError("Определитель существует только у квадратных матриц")
        n = self.rows
        if n == 1:
            return self.data[0][0]
        elif n == 2:
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]
        det = 0
        for j in range(n):
            minor_data = []
            for i in range(1, n):
                minor_row = []
                for k in range(n):
                    if k != j:
                        minor_row.append(self.data[i][k])
                minor_data.append(minor_row)
            minor = Matrix(minor_data)
            det += (-1) ** j * self.data[0][j] * minor.determinant()
        return det
    def inverse(self):
        if not self.is_square():
            raise ValueError("Обратная матрица не определена для неквадратных")
        det = self.determinant()
        if abs(det) < 1e-10:
            raise ValueError("Матрица вырожденная, обратной не существует, так как не определена операция деления на определитель, равный нулю")
        n = self.rows
        if n == 1:
            return Matrix([[1 / self.data[0][0]]])
        # Матрица алгебраических дополнений
        cofactors = []
        for i in range(n):
            cofactor_row = []
            for j in range(n):
                # Минор M_ij
                minor_data = []
                for x in range(n):
                    minor_row = []
                    if x != i:
                        for y in range(n):
                            if y != j:
                                minor_row.append(self.data[x][y])
                        minor_data.append(minor_row)
                minor = Matrix(minor_data)
                # Алгебраическое дополнение A_ij = (-1)^(i+j) * det(M_ij)
                cofactor = (-1) ** (i + j) * minor.determinant()
                cofactor_row.append(cofactor)
            cofactors.append(cofactor_row)
        # Транспонированная матрица алгебраических дополнений (союзная матрица)
        adjugate = Matrix(cofactors).transpose()
        # Обратная матрица = союзная матрица / определитель
        return adjugate * (1 / det)
   
