"""
МОДУЛЬ ВВОДА/ВЫВОДА
Только общение с пользователем, только работа с файлами
НИКАКИХ вычислений!
"""

def input_matrix_interactive():
    """
    Ввод матрицы с клавиатуры
    Возвращает: список списков (например, [[1,2], [3,4]])
    """
    print("\n" + "="*40)
    print(" ВВОД МАТРИЦЫ С КЛАВИАТУРЫ ")
    print("="*40)
    
    # 1. Запрашиваем размер
    while True:
        try:
            rows = int(input("Количество строк: "))
            cols = int(input("Количество столбцов: "))
            
            if rows <= 0 or cols <= 0:
                print("❌ Размер должен быть положительным числом")
                continue
                
            break
        except ValueError:
            print("❌ Введите целое число!")
    
    print(f"\nВведите матрицу {rows}x{cols} построчно.")
    print("Пример: для строки '1 2 3' введите: 1 2 3")
    
    matrix = []
    
    # 2. Вводим строки
    for i in range(rows):
        while True:
            try:
                line = input(f"Строка {i+1}: ").strip()
                
                # Разбиваем на числа
                numbers = line.split()
                if len(numbers) != cols:
                    print(f"❌ Нужно ввести ровно {cols} чисел!")
                    continue
                
                # Преобразуем в числа
                row = []
                for num in numbers:
                    # Пробуем int, если не получается - float
                    try:
                        row.append(int(num))
                    except ValueError:
                        row.append(float(num))
                
                matrix.append(row)
                break
                
            except ValueError:
                print("❌ Введите числа, разделенные пробелами!")
    
    print(f"✓ Матрица {rows}x{cols} успешно введена")
    return matrix


def input_matrix_from_file():
    """
    Чтение матрицы из файла
    Возвращает: список списков или None при ошибке
    """
    print("\n" + "="*40)
    print(" ЧТЕНИЕ МАТРИЦЫ ИЗ ФАЙЛА ")
    print("="*40)
    
    filename = input("Имя файла: ")
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            matrix = []
            
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:  # Пропускаем пустые строки
                    continue
                
                try:
                    # Преобразуем строку в числа
                    row = []
                    for num in line.split():
                        try:
                            row.append(int(num))
                        except ValueError:
                            row.append(float(num))
                    
                    matrix.append(row)
                    
                except ValueError:
                    print(f"❌ Ошибка в строке {line_num}: '{line}'")
                    return None
            
            if not matrix:
                print("❌ Файл пуст!")
                return None
            
            # Проверяем, что все строки одинаковой длины
            first_len = len(matrix[0])
            for i, row in enumerate(matrix):
                if len(row) != first_len:
                    print(f"❌ Строка {i+1} имеет {len(row)} элементов, а должно быть {first_len}")
                    return None
            
            print(f"✓ Матрица {len(matrix)}x{first_len} успешно загружена")
            return matrix
            
    except FileNotFoundError:
        print(f"❌ Файл '{filename}' не найден!")
        return None
    except Exception as e:
        print(f"❌ Ошибка при чтении файла: {e}")
        return None


def print_matrix(matrix, title=""):
    """
    Красивый вывод матрицы
    Принимает: список списков или объект с атрибутом .data
    """
    if title:
        print(f"\n{title}")
        print("=" * 40)
    
    # Если это объект с атрибутом data (например, Matrix)
    if hasattr(matrix, 'data'):
        matrix = matrix.data
    
    if not matrix:
        print("Пустая матрица")
        return
    
    # Определяем максимальную длину числа для красивого вывода
    max_len = 0
    for row in matrix:
        for val in row:
            length = len(f"{val:.3f}")  # Форматируем с 3 знаками после запятой
            if length > max_len:
                max_len = length
    
    # Выводим матрицу
    for row in matrix:
        formatted_row = []
        for val in row:
            if isinstance(val, float):
                # Для красивых дробей
                if val.is_integer():
                    formatted_val = f"{int(val):{max_len}}"
                else:
                    formatted_val = f"{val:{max_len}.3f}"
            else:
                formatted_val = f"{val:{max_len}}"
            formatted_row.append(formatted_val)
        
        print("  ".join(formatted_row))


def save_matrix_to_file(matrix, filename=None):
    """
    Сохранение матрицы в файл
    """
    if filename is None:
        filename = input("Имя файла для сохранения: ")
    
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for row in matrix:
                # Преобразуем все в строки
                line = " ".join(str(x) for x in row)
                file.write(line + "\n")
        
        print(f"✓ Матрица сохранена в '{filename}'")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при сохранении: {e}")
        return False


def ask_save_result(matrix):
    """
    Спросить пользователя, сохранить ли результат
    """
    save = input("\n💾 Сохранить результат в файл? (y/n): ").lower()
    
    if save == 'y':
        filename = input("Имя файла: ")
        save_matrix_to_file(matrix, filename)


def input_scalar():
    """
    Ввод числа (скаляра)
    """
    while True:
        try:
            value = input("Введите число: ")
            # Пробуем int, потом float
            try:
                return int(value)
            except ValueError:
                return float(value)
        except ValueError:
            print("❌ Введите число!")


def get_matrix_source(prompt="матрицу"):
    """
    Спросить, откуда взять матрицу
    Возвращает: 'k' (клавиатура) или 'f' (файл)
    """
    while True:
        source = input(f"\n{prompt.capitalize()}: с клавиатуры (k) или из файла (f)? ").lower()
        
        if source in ['k', 'f']:
            return source
        else:
            print("❌ Введите 'k' или 'f'")
