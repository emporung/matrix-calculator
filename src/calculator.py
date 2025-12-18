from io_handler import *
from matrix import Matrix

class Calculator:
    """Организатор всех матричных операций"""
    
    @staticmethod
    def get_matrix(prompt="матрицу"):
        """Получить матрицу от пользователя -> объект Matrix"""
        source = get_matrix_source(prompt)
        
        if source == 'k':
            data = input_matrix_interactive()
        else:  # 'f'
            data = input_matrix_from_file()
        
        if data is None:
            return None
        
        return Matrix(data)
    
    @staticmethod
    def add_matrices():
        """Сложение матриц"""
        print("\n" + "="*40)
        print(" СЛОЖЕНИЕ МАТРИЦ ")
        print("="*40)
        
        print("\nПервая матрица:")
        A = Calculator.get_matrix("первую матрицу")
        if A is None:
            return
        
        print("\nВторая матрица:")
        B = Calculator.get_matrix("вторую матрицу")
        if B is None:
            return
        
        try:
            result = A + B
            print_matrix(result, "Результат сложения")
            ask_save_result(result.data)
            
        except ValueError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
    
    @staticmethod
    def subtract_matrices():
        """Вычитание матриц"""
        print("\n" + "="*40)
        print(" ВЫЧИТАНИЕ МАТРИЦ ")
        print("="*40)
        
        print("\nПервая матрица (из которой вычитаем):")
        A = Calculator.get_matrix("первую матрицу")
        if A is None:
            return
        
        print("\nВторая матрица (которую вычитаем):")
        B = Calculator.get_matrix("вторую матрицу")
        if B is None:
            return
        
        try:
            result = A - B
            print_matrix(result, "Результат вычитания")
            ask_save_result(result.data)
            
        except ValueError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
    
    @staticmethod
    def multiply_matrices():
        """Умножение матриц"""
        print("\n" + "="*40)
        print(" УМНОЖЕНИЕ МАТРИЦ ")
        print("="*40)
        
        print("\nПервая матрица:")
        A = Calculator.get_matrix("первую матрицу")
        if A is None:
            return
        
        print("\nВторая матрица:")
        B = Calculator.get_matrix("вторую матрицу")
        if B is None:
            return
        
        try:
            result = A * B
            print_matrix(result, "Результат умножения")
            ask_save_result(result.data)
            
        except ValueError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
    
    @staticmethod
    def scalar_multiply():
        """Умножение матрицы на число"""
        print("\n" + "="*40)
        print(" УМНОЖЕНИЕ МАТРИЦЫ НА ЧИСЛО ")
        print("="*40)
        
        A = Calculator.get_matrix("матрицу")
        if A is None:
            return
        
        scalar = input_scalar()
        
        try:
            result = A * scalar
            print_matrix(result, f"Результат умножения на {scalar}")
            ask_save_result(result.data)
            
        except Exception as e:
            print(f"Ошибка: {e}")
    
    @staticmethod
    def transpose():
        """Транспонирование матрицы"""
        print("\n" + "="*40)
        print(" ТРАНСПОНИРОВАНИЕ МАТРИЦЫ ")
        print("="*40)
        
        A = Calculator.get_matrix("матрицу")
        if A is None:
            return
        
        try:
            result = A.transpose()
            print_matrix(result, "Транспонированная матрица")
            ask_save_result(result.data)
            
        except Exception as e:
            print(f"Ошибка: {e}")
    
    @staticmethod
    def determinant():
        """Вычисление определителя"""
        print("\n" + "="*40)
        print(" ВЫЧИСЛЕНИЕ ОПРЕДЕЛИТЕЛЯ ")
        print("="*40)
        
        A = Calculator.get_matrix("матрицу")
        if A is None:
            return
        
        try:
            det = A.determinant()
            print(f"\nОпределитель матрицы: {det}")
            print_matrix(A, "Исходная матрица")
            save = input("\nСохранить результат в файл? (y/n): ").lower()
            if save == 'y':
                filename = input("Имя файла: ")
                with open(filename, 'w') as f:
                    f.write("Определитель матрицы:\n")
                    for row in A.data:
                        f.write(" ".join(str(x) for x in row) + "\n")
                    f.write(f"\nОпределитель: {det}\n")
                print(f"Результат сохранен в '{filename}'")
                
        except ValueError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
    
    @staticmethod
    def inverse():
        """Вычисление обратной матрицы"""
        print("\n" + "="*40)
        print(" ОБРАТНАЯ МАТРИЦА ")
        print("="*40)
        
        A = Calculator.get_matrix("матрицу")
        if A is None:
            return
        
        try:
            result = A.inverse()
            print_matrix(result, "Обратная матрица")
            ask_save_result(result.data)
            
        except ValueError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
    
    @staticmethod
    def trace():
        """Вычисление следа матрицы"""
        print("\n" + "="*40)
        print(" СЛЕД МАТРИЦЫ ")
        print("="*40)
        
        A = Calculator.get_matrix("матрицу")
        if A is None:
            return
        
        try:
            trace_val = A.trace()  # Используем trace из matrix.py
            print(f"\nСлед матрицы: {trace_val}")
            print_matrix(A, "Исходная матрица")
            save = input("\nСохранить результат в файл? (y/n): ").lower()
            if save == 'y':
                filename = input("Имя файла: ")
                with open(filename, 'w') as f:
                    f.write("След матрицы:\n")
                    for row in A.data:
                        f.write(" ".join(str(x) for x in row) + "\n")
                    f.write(f"\nСлед (trace): {trace_val}\n")
                print(f"Результат сохранен в '{filename}'")
                
        except ValueError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
    
    @staticmethod
    def rank():
        """Вычисление ранга матрицы"""
        print("\n" + "="*40)
        print(" РАНГ МАТРИЦЫ ")
        print("="*40)
        
        A = Calculator.get_matrix("матрицу")
        if A is None:
            return
        
        try:
            rank_val = A.rank()
            print(f"\nРанг матрицы: {rank_val}")
            
            print_matrix(A, "Исходная матрица")
            
            save = input("\nСохранить результат в файл? (y/n): ").lower()
            if save == 'y':
                filename = input("Имя файла: ")
                with open(filename, 'w') as f:
                    f.write("Ранг матрицы:\n")
                    for row in A.data:
                        f.write(" ".join(str(x) for x in row) + "\n")
                    f.write(f"\nРанг (rank): {rank_val}\n")
                print(f"Результат сохранен в '{filename}'")
                
        except Exception as e:
            print(f"Ошибка: {e}")
    
    @staticmethod
    def solve_system():
        """Решение СЛАУ"""
        print("\n" + "="*40)
        print(" РЕШЕНИЕ СИСТЕМЫ ЛИНЕЙНЫХ УРАВНЕНИЙ ")
        print("="*40)
        
        print("\nМатрица коэффициентов A:")
        A = Calculator.get_matrix("матрицу коэффициентов")
        if A is None:
            return
        
        print("\nВектор правой части b:")
        try:
            n = A.rows
            print(f"Введите {n} элементов вектора b:")
            b = []
            for i in range(n):
                while True:
                    try:
                        val = float(input(f"b[{i+1}]: "))
                        b.append(val)
                        break
                    except ValueError:
                        print("Введите число!")
        except Exception as e:
            print(f"Ошибка ввода вектора: {e}")
            return
        
        try:
            need_fsr = input("\nНайти ФСР для соотвествующей ОСЛАУ? (y/n): ").lower() == 'y'
            
            if need_fsr:
                solution = A.solve_system(b, return_fsr=True)
                if isinstance(solution, tuple):
                    x_part, fsr, free_vars = solution
                    
                    print("\n=== ЧАСТНОЕ РЕШЕНИЕ ===")
                    for i, val in enumerate(x_part):
                        print(f"x{i+1} = {val:.6f}")
                    
                    print(f"\nСвободные переменные: x{', x'.join(str(v+1) for v in free_vars)}")
                    
                    if fsr:
                        print("\n=== ФУНДАМЕНТАЛЬНАЯ СИСТЕМА РЕШЕНИЙ ===")
                        for i, vec in enumerate(fsr):
                            print(f"v{i+1} = [{', '.join(f'{v:.6f}' for v in vec)}]")
                else:
                    print("\n=== ЕДИНСТВЕННОЕ РЕШЕНИЕ ===")
                    for i, val in enumerate(solution):
                        print(f"x{i+1} = {val:.6f}")
            else:
                solution = A.solve_system(b, return_fsr=False)
                print("\n=== РЕШЕНИЕ ===")
                for i, val in enumerate(solution):
                    print(f"x{i+1} = {val:.6f}")
                    
        except ValueError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
