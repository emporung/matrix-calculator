
class Matrix:
    """Класс для работы с матрицами.
    
    Предоставляет базовые операции линейной алгебры: сложение, вычитание,
    умножение, транспонирование, вычисление определителя, следа, ранга,
    обратной матрицы и решение систем линейных уравнений.
    
    Attributes:
        data (list[list[float]]): Двумерный список элементов матрицы.
        rows (int): Количество строк в матрице.
        cols (int): Количество столбцов в матрице.
    """
    def __init__(self, data):
        """Инициализирует матрицу из двумерного списка.
        
        Args:
            data (list[list[float]]): Двумерный список чисел.
        
        Raises:
            ValueError: Если data пустой, не является списком списков
                или строки имеют разную длину.
        """
        if not data or not all(isinstance(row, list) for row in data):
            raise ValueError("Матрица должна быть непустым списком списков")
        if len(set(len(row) for row in data)) != 1:
            raise ValueError("Строки матрицы должны быть одинаковх размеров")
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])
    
    def __add__(self, other):
        """Сложение двух матриц.
        
        Args:
            other (Matrix): Матрица для сложения.
        
        Returns:
            Matrix: Новая матрица - результат сложения.
        
        Raises:
            ValueError: Если размеры матриц не совпадают.
        
        """
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
        """Вычитание двух матриц.
        
        Args:
            other (Matrix): Матрица для вычитания.
        
        Returns:
            Matrix: Новая матрица - результат вычитания.
        
        Raises:
            ValueError: Если размеры матриц не совпадают.
        """
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
        """Умножение матрицы на число или другую матрицу.
        
        Args:
            other (int, float или Matrix): Множитель.
        
        Returns:
            Matrix: Новая матрица - результат умножения.
        
        Raises:
            ValueError: Если при умножении матриц количество столбцов первой
                не равно количеству строк второй.
        
        Example:
            >>> m = Matrix([[1, 2], [3, 4]])
            >>> (m * 2).data
            [[2, 4], [6, 8]]
            >>> m2 = Matrix([[5, 6], [7, 8]])
            >>> (m * m2).data
            [[19, 22], [43, 50]]
        """
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
                raise ValueError(f"Нельзя умножить матрицы таких размеров: {self.cols} столбцов != {other.rows} строк")
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
        """Проверяет, является ли матрица квадратной.
        
        Returns:
            bool: True если матрица квадратная (rows == cols), иначе False.
        
        """
        return self.rows == self.cols    
    def transpose(self):
        """Транспонирует матрицу.
        
        Returns:
            Matrix: Новая матрица - транспонированная версия текущей.
        
        """
        result = []
        for j in range(self.cols):
            row = []
            for i in range(self.rows):
                row.append(self.data[i][j])
            result.append(row)    
        return Matrix(result)
    
    def gaussian_elimination(self, normalize=False, eps=1e-12):
        """Выполняет метод Гаусса для приведения матрицы к ступенчатому виду.
    
        Реализует алгоритм гауссова исключения (прямой ход) для приведения матрицы
        к ступенчатому виду.
        
        Args:
            normalize: Если True, выполняет нормализацию строк,
                приводя ведущие элементы к 1.
                Если False, оставляет ведущие элементы как есть.
                По умолчанию False.
            eps: Пороговое значение для сравнения чисел с нулём.
                Элементы с абсолютным значением меньше eps считаются нулевыми.
                По умолчанию 1e-12.
        
        Returns:
            Кортеж (Matrix, int), где:
                - Matrix: Матрица в ступенчатом виде
                - int: Количество выполненных перестановок строк
        """
        matrix = [row[:] for row in self.data]
        swaps = 0
        row = col = 0
        
        while row < self.rows and col < self.cols:
            # Ищем первый ненулевой (по модулю > eps) в столбце col
            pivot_row = None
            for k in range(row, self.rows):
                if abs(matrix[k][col]) > eps:
                    pivot_row = k
                    break
            
            if pivot_row is None:  # Весь столбец нулевой
                col += 1
                continue
            
            if pivot_row != row:  # Меняем строки
                matrix[row], matrix[pivot_row] = matrix[pivot_row], matrix[row]
                swaps += 1
            
            if normalize:
                pivot = matrix[row][col]
                if abs(pivot) > eps:
                    matrix[row] = [x / pivot for x in matrix[row]]
                else:
                    # Если после перестановки pivot всё ещё ~0, пропускаем
                    col += 1
                    continue
            
            # Обнуляем элементы ниже pivot
            for k in range(row + 1, self.rows):
                if abs(matrix[k][col]) <= eps:
                    continue
                
                if normalize:
                    factor = matrix[k][col]  # pivot уже = 1
                else:
                    factor = matrix[k][col] / matrix[row][col]
                
                for j in range(col, self.cols):
                    matrix[k][j] -= factor * matrix[row][j]
            
            row += 1
            col += 1
        
        return Matrix(matrix), swaps

    def determinant(self):
        """Вычисляет определитель матрицы.
        
        Returns:
            float: Значение определителя.
        
        Raises:
            ValueError: Если матрица не квадратная.
        
        Example:
            >>> m = Matrix([[1, 2], [3, 4]])
            >>> m.determinant()
            -2.0
        """
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
        if swaps % 2 == 1:
            det = -det
        return det
    
    def inverse(self):
        """Находит обратную матрицу.
        
        Returns:
            Matrix: Обратная матрица.
        
        Raises:
            ValueError: Если матрица не квадратная или вырожденная (null determinant).
        
        Example:
            >>> m = Matrix([[4, 7], [2, 6]])
            >>> inv = m.inverse()
            >>> inv.data
            [[0.6, -0.7], [-0.2, 0.4]]
        """
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
        matrix = [row[:] for row in echelon.data]
        for i in range(n-1, -1, -1):
            for k in range(i-1, -1, -1):
                factor = matrix[k][i]
                for j in range(2*n):
                    matrix[k][j] -= factor * matrix[i][j]
        inverse_data = [matrix[i][n:] for i in range(n)]
        return Matrix(inverse_data)
    
    def trace(self):
        """Вычисляет след матрицы.
        
        Returns:
            float: След матрицы.
        
        Raises:
            ValueError: Если матрица не квадратная.
        """ 
        if not self.is_square():
            raise ValueError("След не существует у неквадратных матриц")
        trace_sum = 0
        for i in range(self.rows):
            trace_sum += self.data[i][i]
        return trace_sum
    def rank(self):
        """Вычисляет ранг матрицы.
        
        Returns:
            int: Ранг матрицы.
        """
        echelon, _ = self.gaussian_elimination(normalize=False)
        rank = 0
        for i in range(min(self.rows, self.cols)):
            if any(abs(echelon.data[i][j]) > 1e-10 for j in range(self.cols)):
                rank += 1
        return rank

    def solve_system(self, b, return_fsr=False):
        """Решает систему линейных уравнений Ax = b.
        
        Args:
            b (list[float]): Вектор свободных членов.
            return_fsr (bool, optional): Если True, возвращает также фундаментальную
                систему решений для однородной системы. По умолчанию False.
        
        Returns:
            Если return_fsr=False:
                list[float]: Вектор решения системы.
            Если return_fsr=True и система имеет бесконечно много решений:
                tuple[list[float], list[list[float]], list[int]]: Кортеж из:
                    - list[float]: Частное решение неоднородной системы
                    - list[list[float]]: Фундаментальная система решений
                    - list[int]: Индексы свободных переменных
        
        Raises:
            ValueError: Если размерность вектора b не соответствует матрице,
                или система несовместна.
        
        Example:
            >>> m = Matrix([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]])
            >>> b = [8, -11, -3]
            >>> m.solve_system(b)
            [2.0, 3.0, -1.0]
        """
        if self.rows != len(b):
            raise ValueError("Размерность вектора b не соответствует матрице A")
        n = self.rows
        m = self.cols
        augmented_data = [self.data[i] + [float(b[i])] for i in range(n)]
        augmented = Matrix(augmented_data)
        echelon, _ = augmented.gaussian_elimination(normalize=True)
        matrix = echelon.data
        for i in range(n):
            if all(abs(matrix[i][j]) < 1e-12 for j in range(m)) and abs(matrix[i][m]) > 1e-12:
                raise ValueError("Система несовместна")
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
        x_part = [0.0] * m
        for idx in range(rank - 1, -1, -1):
            i = idx  # номер строки
            j = basis_vars[idx]  # номер переменной
            x_part[j] = matrix[i][m]  # начинаем с правой части
            # Вычитаем вклады базисных переменных справа
            for k in range(j + 1, m):
                x_part[j] -= matrix[i][k] * x_part[k]
        
        if not free_vars or not return_fsr:
            return x_part
        
        fsr = []
        for free_var in free_vars:
            x = [0.0] * m
            x[free_var] = 1.0
            for i in range(rank - 1, -1, -1):
                basis_var = basis_vars[i]
                
                x[basis_var] = 0.0
                for k in range(basis_var + 1, m):
                    x[basis_var] -= matrix[i][k] * x[k]
                x[basis_var] /= matrix[i][basis_var]
            fsr.append(x)
        
        return x_part, fsr, free_vars
