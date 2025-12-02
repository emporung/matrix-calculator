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
   
    def gaussian_elimination(self):
        if self.rows == 0 or self.cols == 0:
            return Matrix(self.data), 0
        matrix = [row[:] for row in self.data]
        swaps = 0
        for i in range(min(self.rows, self.cols)):
            # Поиск опорного элемента
            pivot_row = i
            for k in range(i, self.rows):
                if abs(matrix[k][i]) > 1e-12:
                    pivot_row = k
                    break
            if abs(matrix[pivot_row][i]) < 1e-12:
                continue  # весь столбец нулевой
            # Перестановка строк
            if pivot_row != i:
                matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
                swaps += 1
        # Зануление элементов ниже
        for k in range(i + 1, self.rows):
            factor = matrix[k][i] / matrix[i][i]
            for j in range(i, self.cols):
                matrix[k][j] -= factor * matrix[i][j]
    return Matrix(matrix), swaps

    def determinant(self):
        if not self.is_square():
            raise ValueError("Определитель существует только у квадратных матриц")
        echelon, swaps = self.gaussian_elimination()
        det = 1.0
        for i in range(self.rows):
            det *= echelon.data[i][i]
        if swaps % 2 == 1:  # нечётное число перестановок
            det = -det
        return det
    
    def inverse(self):
        if not self.is_square():
            raise ValueError("Обратная матрица не определена для неквадратных")
        n = self.rows
        det = self.determinant()
        if abs(det) < 1e-10:
            raise ValueError("Матрица вырожденная, обратной не существует")
        augmented_data = []
        for i in range(n):
            left_part = self.data[i]
            right_part = [1.0 if j == i else 0.0 for j in range(n)]
            augmented_data.append(left_part + right_part)
        augmented = Matrix(augmented_data)
        echelon, _ = augmented.gaussian_elimination()
        # Обратный ход метода Гаусса-Жордана
        matrix = [row[:] for row in echelon.data]  # глубокая копия!
        for i in range(n-1, -1, -1):
            # Нормализация диагонального элемента до 1
            pivot = matrix[i][i]
            for j in range(2*n):
                matrix[i][j] /= pivot
            # Зануление элементов выше в столбце i
            for k in range(i-1, -1, -1):
                factor = matrix[k][i]
                for j in range(2*n):
                    matrix[k][j] -= factor * matrix[i][j]
        # обратную матрицу (правая половина)
        inverse_data = [matrix[i][n:] for i in range(n)]
        return Matrix(inverse_data)     
   
