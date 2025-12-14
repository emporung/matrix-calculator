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
   
    def gaussian_elimination(self, normalize=False):
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
            if normalize:
                # Нормализуем текущую строку
                pivot = matrix[i][i]
                for j in range(i, self.cols):
                    matrix[i][j] /= pivot
            # Зануление элементов ниже
            for k in range(i + 1, self.rows):
                factor = matrix[k][i] / (matrix[i][i] if not normalize else 1.0)
                for j in range(i, self.cols):
                    matrix[k][j] -= factor * matrix[i][j]
        return Matrix(matrix), swaps

    def determinant(self):
        if not self.is_square():
            raise ValueError("Определитель существует только у квадратных матриц")
        n = self.rows
        for i in range(n):
            if all(abs(self.data[i][j]) < 1e-12 for j in range(n)):
                return 0.0
        for j in range(n):
            if all(abs(self.data[i][j]) < 1e-12 for i in range(n)):
                return 0.0
        echelon, swaps = self.gaussian_elimination(normalize=False)
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
        echelon, _ = augmented.gaussian_elimination(normalize=True)
        # Обратный ход метода Гаусса-Жордана
        matrix = [row[:] for row in echelon.data]  # глубокая копия!
        for i in range(n-1, -1, -1):
            
            # Зануление элементов выше в столбце i
            for k in range(i-1, -1, -1):
                factor = matrix[k][i]
                for j in range(2*n):
                    matrix[k][j] -= factor * matrix[i][j]
        # обратную матрицу (правая половина)
        inverse_data = [matrix[i][n:] for i in range(n)]
        return Matrix(inverse_data)
    def trace(self):
        if not self.is_square():
            raise ValueError("След не существует у неквадратных матриц")
        
        trace_sum = 0
        for i in range(self.rows):
            trace_sum += self.data[i][i]
        return trace_sum
    def rank(self):
        echelon, _ = self.gaussian_elimination(normalize=False)
        rank = 0
        for i in range(min(self.rows, self.cols)):
            if any(abs(echelon.data[i][j]) > 1e-10 for j in range(self.cols)):
                rank += 1
        return rank

    def solve_system(self, b, return_fsr=False):
        
        if self.rows != len(b):
            raise ValueError("Размерность вектора b не соответствует матрице A")
        
        n = self.rows
        m = self.cols
        # 1. Создаём расширенную матрицу [A|b]
        augmented_data = [self.data[i] + [float(b[i])] for i in range(n)]
        augmented = Matrix(augmented_data)
        
        # 2. Прямой ход Гаусса
        echelon, _ = augmented.gaussian_elimination(normalize=True)
        matrix = echelon.data
        
        # 3. Проверка совместности
        for i in range(n):
            # Если вся строка A нулевая, но b не ноль
            if all(abs(matrix[i][j]) < 1e-12 for j in range(m)) and abs(matrix[i][m]) > 1e-12:
                raise ValueError("Система несовместна")
        
        # 4. Определяем базисные и свободные переменные
        basis_vars = []    
        free_vars = []
        row = 0
        for col in range(m):
            if row < n and abs(matrix[row][col]) > 1e-12:
                basis_vars.append(col)
                row += 1
            else:
                free_vars.append(col)
        
        rank = len(basis_vars)
        
        # 5. Находим ОДНО частное решение
        x_part = [0.0] * m
        
        # Обратный ход для базисных переменных
        for idx in range(rank - 1, -1, -1):
            i = idx  # номер строки
            j = basis_vars[idx]  # номер переменной
            
            x_part[j] = matrix[i][m]  # начинаем с правой части
            
            # Вычитаем вклады базисных переменных справа
            for k in range(j + 1, m):
                x_part[j] -= matrix[i][k] * x_part[k]
        
        # 6. Если решение единственное или не просили ФСР
        if not free_vars or not return_fsr:
            return x_part
        
        # 7. Находим Фундаментальную Систему Решений
        fsr = []
        
        # Для каждой свободной переменной строим вектор ФСР
        for free_idx, free_var in enumerate(free_vars):
            # Вектор решения, где free_var = 1, остальные свободные = 0
            x_fsr = [0.0] * m
            x_fsr[free_var] = 1.0
            
            # Выражаем базисные переменные через свободные
            for idx in range(rank - 1, -1, -1):
                i = idx
                j = basis_vars[idx]
                
                # Начинаем с коэффициента при свободной переменной
                x_fsr[j] = -matrix[i][free_var]
                
                # Вычитаем вклады остальных свободных переменных
                for k in range(j + 1, m):
                    if k in free_vars and k != free_var:
                        x_fsr[j] -= matrix[i][k] * x_fsr[k]
            
            fsr.append(x_fsr)
        
        return x_part, fsr, free_vars
