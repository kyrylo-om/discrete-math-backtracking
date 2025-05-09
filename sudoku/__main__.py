"""
Starting init for the sudoku app for 
"""

import csv
import argparse
from sudoku_cls import Sudoku, sudoku_from_file, test_sudoku
from sudoku_vis import init_visualization

def main():
    """
    Main sudoku module initilization with argparse.
    """
    parser = argparse.ArgumentParser(description="Sudoku Solver")
    parser.add_argument("-f", "--file", type=str, default="")
    parser.add_argument("-s", "--size", type=int, default=0)
    parser.add_argument("-v", "--visualization", action="store_true")

    parser.add_argument("-t", "--test", action="store_true")
    parser.add_argument("--sizes", type=int, nargs="+")
    parser.add_argument("--iters", type=int)
    parser.add_argument("--fill_chances", type=float, nargs="+")
    parser.add_argument("--output_file", type=str)

    args = parser.parse_args()

    if args.test:
        if any([args.file, args.size, args.visualization]):
            print("Error: --file, --size, or --visualization may not be used when running tests.")
            return

        if not all([args.sizes, args.iters, args.fill_chances, args.output_file]):
            print("Error: --sizes, --iters, --fill_chances and --output_file "
                  "must be specified when using --test.")
            return

        print(f"Running tests with sizes={args.sizes}, iters={args.iters}, fill_chances={args.fill_chances}")
        results = test_sudoku(args.sizes, args.iters, args.fill_chances)

        with open("sudoku/"+args.output_file.strip("\""), mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Board Size", "Fill Chance", "Method", "Time (s)"])

            for size, fill_results in results.items():
                for fill, tests in fill_results.items():
                    for method, _, time in tests:
                        writer.writerow([f"{size}x{size}", fill, method, time])

        return

    if args.file and args.size:
        raise ValueError("Error: Only one of file and size arguments must be specified, not both.")

    if args.file:
        try:
            sudoku = sudoku_from_file(args.file)
            print(f"Loaded a Sudoku board of size {sudoku.size}x{sudoku.size} from {args.file}")
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found, exiting.")
            return
    elif args.size:
        sudoku = Sudoku(args.size)
        print(f"No board specified. Created an empty {args.size}x{args.size} Sudoku.")
    else:
        sudoku = Sudoku(9)
        print("No board or size specified. Created an empty 9x9 Sudoku.")

    if args.visualization:
        init_visualization(sudoku)
    else:
        if sudoku.is_board_valid():
            if sudoku.solve():
                print(sudoku)
                print("Solved Board:")
                print(sudoku)
            else:
                print("No solution found for the given board.")
        else:
            print("The provided board is invalid.")

if __name__ == "__main__":
    main()
