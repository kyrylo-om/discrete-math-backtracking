import argparse

def create_parser():
    """Створює та конфігурує парсер аргументів"""
    parser = argparse.ArgumentParser(
        prog="Sudoku Solver",
        description="Програма для розв'язання та аналізу судоку"
    )

    main_group = parser.add_argument_group("Основні параметри")
    main_group.add_argument("-f", "--file", 
                          type=str,
                          default="",
                          help="Шлях до файлу з судоку")
    main_group.add_argument("-s", "--size",
                          type=int,
                          default=0,
                          help="Розмір поля судоку")
    main_group.add_argument("-v", "--visualization",
                          action="store_true",
                          help="Увімкнути візуалізацію")

    test_group = parser.add_argument_group("Тестування")
    test_group.add_argument("-t", "--test",
                          action="store_true",
                          help="Запустити тестові сценарії")
    test_group.add_argument("--sizes",
                          type=int,
                          nargs="+",
                          help="Розміри полів для тестування")
    test_group.add_argument("--iters",
                          type=int,
                          help="Кількість ітерацій тесту")
    test_group.add_argument("--fill_chances",
                          type=float,
                          nargs="+",
                          help="Ймовірності заповнення для тесту")
    test_group.add_argument("--output_file",
                          type=str,
                          help="Файл для збереження результатів тесту")

    return parser