from parser import create_parser


def main():
    """Головна функція програми"""
    parser = create_parser()
    args = parser.parse_args()
    
    print("Отримані аргументи:")
    print(f"Файл: {args.file}")
    print(f"Розмір: {args.size}")
    print(f"Візуалізація: {args.visualization}")

    if args.test:
        handle_test_arguments(args)


def handle_test_arguments(args):
    """Обробка аргументів тестування"""
    print("\nТестові параметри:")
    print(f"Розміри: {args.sizes}")
    print(f"Ітерації: {args.iters}")
    print(f"Ймовірності заповнення: {args.fill_chances}")
    print(f"Вихідний файл: {args.output_file}")


if __name__ == "__main__":
    main()
