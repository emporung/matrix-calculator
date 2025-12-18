def show_menu():
    """Просто показывает меню"""
    print("\n" + "="*50)
    print(" КАЛЬКУЛЯТОР МАТРИЦ ")
    print("="*50)
    print("1.  Сложение матриц")
    print("2.  Вычитание матриц")
    print("3.  Умножение матриц")
    print("4.  Умножение матрицы на число")
    print("5.  Транспонирование")
    print("6.  Определитель")
    print("7.  Обратная матрица")
    print("8.  След матрицы")
    print("9.  Ранг матрицы")
    print("10. Решение СЛАУ")
    print("11. Выйти")
    print("="*50)

def main():
    """Главная функция - ТОЛЬКО УПРАВЛЕНИЕ"""
    print("Добро пожаловать в калькулятор матриц!")
    
    from calculator import Calculator
    
    while True:
        show_menu()
        
        try:
            choice = input("\nВыберите операцию (1-11): ").strip()
            
            if choice == '1':
                Calculator.add_matrices()
            elif choice == '2':
                Calculator.subtract_matrices()
            elif choice == '3':
                Calculator.multiply_matrices()
            elif choice == '4':
                Calculator.scalar_multiply()
            elif choice == '5':
                Calculator.transpose()
            elif choice == '6':
                Calculator.determinant()
            elif choice == '7':
                Calculator.inverse()
            elif choice == '8':
                Calculator.trace()
            elif choice == '9':
                Calculator.rank()
            elif choice == '10':
                Calculator.solve_system()
            elif choice == '11':
                print("\nДо свидания!")
                break
            else:
                print("Неверный выбор. Введите число от 1 до 11.")
                
        except KeyboardInterrupt:
            print("\n\nВыход из программы.")
            break
        except Exception as e:
            print(f"\nОшибка: {e}")

if __name__ == "__main__":
    main()
