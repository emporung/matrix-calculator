import unittest
from matrix import Matrix
class TestMatrix(unittest.TestCase):
    
    def setUp(self):
        """Начальные данные для тестов"""
        self.A = Matrix([[1, 2], [3, 4]])
        self.B = Matrix([[5, 6], [7, 8]])
        self.C = Matrix([[1, 2, 3], [4, 5, 6]])
        self.D = Matrix([[1, 0], [0, 1]])
        self.E = Matrix([[2, 0, 0], [0, 3, 0], [0, 0, 4]])
    
    def test_constructor_valid(self):
        m = Matrix([[1, 2], [3, 4]])
        self.assertEqual(m.rows, 2)
        self.assertEqual(m.cols, 2)
    
    def test_constructor_invalid_empty(self):
        with self.assertRaises(ValueError):
            Matrix([])
    
    def test_constructor_invalid_ragged(self):
        with self.assertRaises(ValueError):
            Matrix([[1, 2], [3]])
    
    def test_addition_valid(self):
        result = self.A + self.B
        expected = Matrix([[6, 8], [10, 12]])
        self.assertEqual(result.data, expected.data)
    
    def test_addition_invalid_sizes(self):
        with self.assertRaises(ValueError):
            self.A + self.C
    
    def test_subtraction_valid(self):
        result = self.B - self.A
        expected = Matrix([[4, 4], [4, 4]])
        self.assertEqual(result.data, expected.data)
    
    def test_subtraction_invalid_sizes(self):
        with self.assertRaises(ValueError):
            self.A - self.C
    
    def test_scalar_multiplication(self):
        result = self.A * 2
        expected = Matrix([[2, 4], [6, 8]])
        self.assertEqual(result.data, expected.data)
    
    def test_scalar_multiplication_float(self):
        result = self.A * 0.5
        expected = Matrix([[0.5, 1.0], [1.5, 2.0]])
        for i in range(2):
            for j in range(2):
                self.assertAlmostEqual(result.data[i][j], expected.data[i][j])
    
    def test_matrix_multiplication_valid(self):
        result = self.A * self.B
        expected = Matrix([[19, 22], [43, 50]])
        self.assertEqual(result.data, expected.data)
    
    def test_multiplication_invalid(self):
        """Минимальный тест для проверки умножения"""
        C = Matrix([[1, 2, 3], [4, 5, 6]])  # 2×3
        A = Matrix([[1, 2], [3, 4]])        # 2×2
       
        with self.assertRaises(ValueError) as cm:
            C * A
        
        error_msg = str(cm.exception)
        # Дополнительная проверка
        self.assertIn("столбцов", error_msg)
        self.assertIn("строк", error_msg)
    
    
    def test_transpose_square(self):
        result = self.A.transpose()
        expected = Matrix([[1, 3], [2, 4]])
        self.assertEqual(result.data, expected.data)
    
    def test_transpose_rectangular(self):
        result = self.C.transpose()
        expected = Matrix([[1, 4], [2, 5], [3, 6]])
        self.assertEqual(result.data, expected.data)
    
    
    def test_determinant_2x2(self):
        det = self.A.determinant()
        self.assertAlmostEqual(det, -2.0)
    
    def test_determinant_3x3(self):
        m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        det = m.determinant()
        self.assertAlmostEqual(det, 0.0)
    
    def test_determinant_diagonal(self):
        det = self.E.determinant()
        self.assertAlmostEqual(det, 24.0)
    
    def test_determinant_zero_row(self):
        m = Matrix([[1, 2], [0, 0]])
        det = m.determinant()
        self.assertAlmostEqual(det, 0.0)
    
    def test_determinant_zero_col(self):
        m = Matrix([[1, 0], [2, 0]])
        det = m.determinant()
        self.assertAlmostEqual(det, 0.0)
    
    def test_determinant_non_square(self):
        with self.assertRaises(ValueError):
            self.C.determinant()
    
   
    def test_inverse_2x2(self):
        result = self.A.inverse()
        expected = Matrix([[-2.0, 1.0], [1.5, -0.5]])
        for i in range(2):
            for j in range(2):
                self.assertAlmostEqual(result.data[i][j], expected.data[i][j])
    
    def test_inverse_identity(self):
        result = self.D.inverse()
        self.assertEqual(result.data, self.D.data)
    
    def test_inverse_singular(self):
        m = Matrix([[1, 2], [2, 4]])
        with self.assertRaises(ValueError):
            m.inverse()
    
    def test_inverse_non_square(self):
        with self.assertRaises(ValueError):
            self.C.inverse()
    
    
    def test_trace_square(self):
        trace = self.A.trace()
        self.assertEqual(trace, 5)
    
    def test_trace_non_square(self):
        with self.assertRaises(ValueError):
            self.C.trace()
    
   
    def test_rank_full(self):
        rank = self.A.rank()
        self.assertEqual(rank, 2)
    
    def test_rank_singular(self):
        m = Matrix([[1, 2], [2, 4]])
        rank = m.rank()
        self.assertEqual(rank, 1)
    
    def test_rank_zero(self):
        m = Matrix([[0, 0], [0, 0]])
        rank = m.rank()
        self.assertEqual(rank, 0)
    
    def test_rank_rectangular(self):
        rank = self.C.rank()
        self.assertEqual(rank, 2)
    
    
    def test_solve_system_unique(self):
        A = Matrix([[2, 1], [1, 3]])
        b = [5, 5]
        x = A.solve_system(b)
        result = A * Matrix([[x[0]], [x[1]]])
        self.assertAlmostEqual(result.data[0][0], b[0], places=10)
        self.assertAlmostEqual(result.data[1][0], b[1], places=10)
    
    def test_solve_system_infinite(self):
        A = Matrix([[1, 1, 1]])
        b = [1]
        x_part = A.solve_system(b, return_fsr=False)
        self.assertAlmostEqual(x_part[0] + x_part[1] + x_part[2], 1.0, places=10)
    
    def test_solve_system_inconsistent(self):
        A = Matrix([[1, 2], [0, 0]])
        b = [1, 1]
        with self.assertRaises(ValueError):
            A.solve_system(b)
    
    def test_solve_system_homogeneous(self):
        A = Matrix([[1, 1, 1], [2, 2, 2]])
        b = [0, 0]
        x_part, fsr, free_vars = A.solve_system(b, return_fsr=True)
        self.assertAlmostEqual(x_part[0], 0.0, places=10)
        self.assertAlmostEqual(x_part[1], 0.0, places=10)
        self.assertAlmostEqual(x_part[2], 0.0, places=10)
        self.assertEqual(len(fsr), len(free_vars))
    
    
    def test_gaussian_elimination_without_normalize(self):
        A = Matrix([[2, 4], [1, 3]])
        echelon, swaps = A.gaussian_elimination(normalize=False)
        self.assertLess(abs(echelon.data[1][0]), 1e-10)
    
    def test_gaussian_elimination_with_normalize(self):
        A = Matrix([[2, 4], [1, 3]])
        echelon, swaps = A.gaussian_elimination(normalize=True)
        self.assertAlmostEqual(echelon.data[0][0], 1.0, places=10)
        self.assertAlmostEqual(echelon.data[1][1], 1.0, places=10)
        self.assertLess(abs(echelon.data[1][0]), 1e-10)
        

    def test_zero_matrix(self):
        zero = Matrix([[0, 0], [0, 0]])
        
        # Сложение
        result = zero + self.A
        self.assertEqual(result.data, self.A.data)
        
        # Умножение на скаляр
        result = zero * 5
        self.assertEqual(result.data, zero.data)
        
        # Определитель
        self.assertAlmostEqual(zero.determinant(), 0.0)
        
        # Ранг
        self.assertEqual(zero.rank(), 0)
        
        # След
        self.assertEqual(zero.trace(), 0)
    
    # Тест с единичной матрицей
    def test_identity_matrix(self):
        I = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        
        # Умножение
        result = I * self.E
        self.assertEqual(result.data, self.E.data)
        
        # Определитель
        self.assertAlmostEqual(I.determinant(), 1.0)
        
        # Обратная
        inv = I.inverse()
        self.assertEqual(inv.data, I.data)
        
        # След
        self.assertEqual(I.trace(), 3)
        
        # Ранг
        self.assertEqual(I.rank(), 3)
    
    # Тест на большие числа
    def test_large_numbers(self):
        m = Matrix([[1e6, 2e6], [3e6, 4e6]])
        
        det = m.determinant()
        expected = 1e6*4e6 - 2e6*3e6
        self.assertAlmostEqual(det, expected, places=2)
        
        trace = m.trace()
        self.assertAlmostEqual(trace, 5e6, places=2)
    
    # Тест на малые числа 
    def test_small_numbers(self):
        m = Matrix([[1e-12, 2e-12], [3e-12, 4e-12]])
        
        # Определитель должен устремиться к 0
        det = m.determinant()
        self.assertLess(abs(det), 1e-20)
        
        # Ранг должен быть 0 (все числа меньше epsilon)
        rank = m.rank()
        self.assertEqual(rank, 0)
    
    # проверка квадратности 
    def test_is_square(self):
        self.assertTrue(self.A.is_square())
        self.assertFalse(self.C.is_square())
   
    
    
    # Тест 1x1 матрицы (краевой случай)
    def test_1x1_matrix(self):
        m = Matrix([[5]])
        
        self.assertEqual(m.determinant(), 5.0)
        self.assertEqual(m.trace(), 5.0)
        self.assertEqual(m.rank(), 1)
        
        inv = m.inverse()
        self.assertAlmostEqual(inv.data[0][0], 0.2)
        
        # СЛАУ 1x1
        x = m.solve_system([10])
        self.assertAlmostEqual(x[0], 2.0)
    
    # Тест прямоугольной системы (больше уравнений чем неизвестных)
    def test_rectangular_solve(self):
        # Больше уравнений чем неизвестных
        A = Matrix([[1, 2], [3, 4], [5, 6]])
        b = [5, 11, 17]
        
        x = A.solve_system(b)
        # Проверяем что решение приблизительно [1, 2]
        self.assertAlmostEqual(x[0], 1.0, places=5)
        self.assertAlmostEqual(x[1], 2.0, places=5)
    
    # Тест недоопределённой системы (меньше уравнений чем неизвестных)
    def test_underdetermined_system(self):
        # Меньше уравнений чем неизвестных
        A = Matrix([[1, 2, 3]])
        b = [6]
        
        x_part, fsr, free_vars = A.solve_system(b, return_fsr=True)
        
        # Проверяем что частное решение удовлетворяет
        self.assertAlmostEqual(x_part[0] + 2*x_part[1] + 3*x_part[2], 6.0)
        
        # Должно быть 2 свободные переменные
        self.assertEqual(len(free_vars), 2)
        self.assertEqual(len(fsr), 2)

if __name__ == '__main__':
    unittest.main(verbosity=2)
