import tkinter as tk
from parser import create_parser
from queens import find_all_queens, BacktrackingVisualizer
CELL_SIZE = 50


def handle_cli_args(args):
    """Обробка аргументів командного рядка"""
    if not all([args.queens, args.rows, args.cols]):
        print("Потрібно вказати всі основні параметри: --queens, --rows, --cols")
        return

    try:
        if args.queens <= 0 or args.rows <= 0 or args.cols <= 0:
            raise ValueError("Значення повинні бути більше 0")
        if args.queens > min(args.rows, args.cols):
            raise ValueError("Неможливо розмістити більше ферзів ніж розмір поля")
    except ValueError as e:
        print(f"Помилка вводу: {str(e)}")
        return

    if args.no_gui:

        solutions = find_all_queens(args.queens, args.rows, args.cols)
        print(f"Знайдено розв'язків: {len(solutions)}")
        if args.output:
            with open(args.output, "w") as f:
                for sol in solutions:
                    f.write(str(sol) + "\n")
    else:
        root = tk.Tk()
        app = BacktrackingVisualizer()
        app.queens_entry.insert(0, str(args.queens))
        app.rows_entry.insert(0, str(args.rows))
        app.cols_entry.insert(0, str(args.cols))
        app.speed_slider.set(args.speed)
        root.mainloop()


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    if any([args.queens, args.rows, args.cols]):
        handle_cli_args(args)
    else:
        BacktrackingVisualizer()
