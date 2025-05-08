import argparse


def create_parser():
    """Створює та конфігурує парсер аргументів"""
    parser = argparse.ArgumentParser(
        prog="N-Queens Visualizer",
        description="Програма для візуалізації розміщення ферзів",
    )

    main_group = parser.add_argument_group("Основні параметри")
    main_group.add_argument(
        "-q", "--queens", type=int, help="Кількість ферзів для розміщення"
    )
    main_group.add_argument("-r", "--rows", type=int, help="Кількість рядків дошки")
    main_group.add_argument("-c", "--cols", type=int, help="Кількість стовпців дошки")

    vis_group = parser.add_argument_group("Візуалізація")
    vis_group.add_argument(
        "-s", "--speed", type=int, default=500, help="Швидкість анімації у мілісекундах"
    )
    vis_group.add_argument(
        "--no-gui", action="store_true", help="Запуск без графічного інтерфейсу"
    )

    output_group = parser.add_argument_group("Експорт")
    output_group.add_argument(
        "-o", "--output", type=str, help="Шлях для збереження результатів у файл"
    )

    return parser
