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
        result = zero + self.A
        self.assertEqual(result.data, self.A.data)
        result = zero * 5
        self.assertEqual(result.data, zero.data)
        self.assertAlmostEqual(zero.determinant(), 0.0)
        self.assertEqual(zero.rank(), 0)
        self.assertEqual(zero.trace(), 0)
    
   
    def test_identity_matrix(self):
        I = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        result = I * self.E
        self.assertEqual(result.data, self.E.data)
        self.assertAlmostEqual(I.determinant(), 1.0)
        inv = I.inverse()
        self.assertEqual(inv.data, I.data)
        self.assertEqual(I.trace(), 3)
        self.assertEqual(I.rank(), 3)
    
    
    def test_large_numbers(self):
        m = Matrix([[1e6, 2e6], [3e6, 4e6]])
        det = m.determinant()
        expected = 1e6*4e6 - 2e6*3e6
        self.assertAlmostEqual(det, expected, places=2)
        trace = m.trace()
        self.assertAlmostEqual(trace, 5e6, places=2)
   
    def test_small_numbers(self):
        m = Matrix([[1e-12, 2e-12], [3e-12, 4e-12]])
        det = m.determinant()
        self.assertLess(abs(det), 1e-20)
        rank = m.rank()
        self.assertEqual(rank, 0)
        
    def test_is_square(self):
        self.assertTrue(self.A.is_square())
        self.assertFalse(self.C.is_square())
    
    def test_1x1_matrix(self):
        m = Matrix([[5]])
        self.assertEqual(m.determinant(), 5.0)
        self.assertEqual(m.trace(), 5.0)
        self.assertEqual(m.rank(), 1)
        inv = m.inverse()
        self.assertAlmostEqual(inv.data[0][0], 0.2)
        x = m.solve_system([10])
        self.assertAlmostEqual(x[0], 2.0)
    
    def test_rectangular_solve_overdetermined(self):
        A = Matrix([[1, 2], [3, 4], [5, 6]])
        b = [5, 11, 17]
        x = A.solve_system(b)
        self.assertAlmostEqual(x[0], 1.0, places=10)
        self.assertAlmostEqual(x[1], 2.0, places=10)
        self.assertAlmostEqual(1*x[0] + 2*x[1], 5.0, places=10)
        self.assertAlmostEqual(3*x[0] + 4*x[1], 11.0, places=10)
        self.assertAlmostEqual(5*x[0] + 6*x[1], 17.0, places=10)
    
    def test_rectangular_solve_overdetermined_inconsistent(self):
        A = Matrix([[1, 2], [3, 4], [5, 6]])
        b = [5, 11, 18]
        with self.assertRaises(ValueError) as context:
            A.solve_system(b)
        self.assertIn("несовмест", str(context.exception).lower())
    
    def test_underdetermined_system(self):
        A = Matrix([[1, 2, 3]])
        b = [6]
        x_part, fsr, free_vars = A.solve_system(b, return_fsr=True)
        computed = x_part[0] + 2*x_part[1] + 3*x_part[2]
        self.assertAlmostEqual(computed, 6.0, places=10,
                              msg=f"Частное решение {x_part} не удовлетворяет уравнению")
        self.assertEqual(len(free_vars), 2, 
                        f"Ожидалось 2 свободные переменные, получили {len(free_vars)}")
        self.assertEqual(len(fsr), 2,
                        f"Ожидалось 2 вектора ФСР, получили {len(fsr)}")
        for i, vec in enumerate(fsr):
            homogeneous_check = vec[0] + 2*vec[1] + 3*vec[2]
            self.assertAlmostEqual(homogeneous_check, 0.0, places=10,
                                  msg=f"Вектор ФСР {i} {vec} не удовлетворяет однородной системе")
        import random
        for _ in range(5):  # Проверяем 5 случайных комбинаций
            c1 = random.uniform(-10, 10)
            c2 = random.uniform(-10, 10)
            
            x_general = [
                x_part[0] + c1*fsr[0][0] + c2*fsr[1][0],
                x_part[1] + c1*fsr[0][1] + c2*fsr[1][1],
                x_part[2] + c1*fsr[0][2] + c2*fsr[1][2]
            ]
            
            computed = x_general[0] + 2*x_general[1] + 3*x_general[2]
            self.assertAlmostEqual(computed, 6.0, places=10,
                                  msg=f"Общее решение с c1={c1}, c2={c2} не удовлетворяет")
    
    def test_underdetermined_system_zero_rhs(self):
        A = Matrix([[1, 2, 3]])
        b = [0]
        x_part, fsr, free_vars = A.solve_system(b, return_fsr=True)
        norm = sum(abs(x) for x in x_part)
        self.assertLess(norm, 1e-10, 
                       f"Частное решение должно быть нулевым, получили {x_part}")
        self.assertEqual(len(fsr), 2)
        for vec in fsr:
            check = vec[0] + 2*vec[1] + 3*vec[2]
            self.assertAlmostEqual(check, 0.0, places=10)
    
    def test_square_system_unique_solution(self):
        A = Matrix([[2, 1], [1, -1]])
        b = [5, 1]
        x = A.solve_system(b)
        
        self.assertAlmostEqual(x[0], 2.0, places=10)
        self.assertAlmostEqual(x[1], 1.0, places=10)
        
        self.assertAlmostEqual(2*x[0] + x[1], 5.0, places=10)
        self.assertAlmostEqual(x[0] - x[1], 1.0, places=10)
    
    def test_singular_system(self):
        A = Matrix([[1, 1], [2, 2]])
        b = [3, 6]
        x_part, fsr, free_vars = A.solve_system(b, return_fsr=True)
        self.assertEqual(len(free_vars), 1)
        self.assertEqual(len(fsr), 1)
        self.assertAlmostEqual(x_part[0] + x_part[1], 3.0, places=10)
    
    def test_singular_system_inconsistent(self):
        A = Matrix([[1, 1], [2, 2]])
        b = [3, 7]
        with self.assertRaises(ValueError) as context:
            A.solve_system(b)
        self.assertIn("несовмест", str(context.exception).lower())

if __name__ == '__main__':
    unittest.main(verbosity=2)
