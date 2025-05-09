"""
Sudoku algorithm
"""

from __future__ import annotations
from math import log10, ceil
from random import random, shuffle
import time
from copy import deepcopy
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sudoku_vis import SudokuVis


class UserAbortedError(Exception):
    """Error for exiting out of sudoku visualization."""

class Sudoku:
    """
    Sudoku implementation.
    """
    def __init__(self, board=9):
        if isinstance(board, int):
            self.size = board
            self.board = [[None] * self.size for _ in range(self.size)]

        elif isinstance(board, list):
            self.board = board

            self.size = len(self.board)

            if any(self.size != len(row) for row in self):
                raise ValueError("Board width and height should be the same.")
        else:
            raise TypeError

        self.grid_width = get_closest_grid(self.size)
        self.grid_height = self.size//self.grid_width

        self.cell_order = []

        self.stop_solve = False

        self.generate_cell_order()

    def __iter__(self):
        return iter(self.board)

    def __getitem__(self, index):
        return self.board[index]

    def get_valid_numbers(self, row, col):
        """
        Returns a list of all valid numbers for the given cell.
        """
        invalid_numbers = set()

        start_row = row // self.grid_height * self.grid_height
        start_col = col // self.grid_width * self.grid_width

        for i in range(self.size):
            invalid_numbers.add(self[row][i])

            invalid_numbers.add(self[i][col])

            invalid_numbers.add(self[start_row+i%self.grid_height][start_col+i//self.grid_width])


        return [num for num in range(1, self.size + 1) if num not in invalid_numbers]

    def find_next_cell(self):
        """
        Finds the next empty cell with the fewest valid options.
        """
        for row, col in self.cell_order:
            if self[row][col] is None:
                return (row, col)

        return None

    def solve(self, greedy = False, visualization: SudokuVis | None = None, random_fill=False):
        """
        Solves the Sudoku board using DFS with optimized valid number calculation.
        """
        if self.stop_solve:
            self.stop_solve = False
            raise StopIteration

        if greedy:
            self.generate_cell_order(greedy=True)

        cell = self.find_next_cell()

        if cell is None:
            return True

        row, col = cell

        valid_numbers = self.get_valid_numbers(row, col)

        if random_fill:
            shuffle(valid_numbers)

        for num in valid_numbers:
            self[row][col] = num

            if visualization:
                visualization.update_cell(row, col, num)

            if self.solve(greedy=greedy, visualization=visualization, random_fill=random_fill):
                return True

            self[row][col] = None

            if visualization:
                visualization.update_cell(row, col, "")

        return False

    def is_board_valid(self):
        """
        Returns true or false depending on if the board is valid.
        """
        rows = {i: set() for i in range(self.size)}
        columns = {i: set() for i in range(self.size)}

        for i in range(self.size):
            for j in range(self.size):
                cell = self[i][j]
                if cell is None:
                    continue

                if not 1 <= cell <= self.size:
                    return False

                if cell in rows[i]:
                    return False

                rows[i].add(cell)

                if cell in columns[j]:
                    return False

                columns[j].add(cell)

        for row_start in range(self.grid_width):
            for col_start in range(self.grid_height):
                grid = set()

                for i in range(self.grid_height):
                    for j in range(self.grid_width):
                        cell = self[row_start*self.grid_height+i][col_start*self.grid_width+j]

                        if cell is None:
                            continue

                        if cell in grid:
                            return False

                        grid.add(cell)

        return True

    def generate_cell_order(self, greedy=False):
        """
        Returns a sorted list cell ordered by cells that have the least options.
        """
        cells=[(i,j)for i in range(self.size) for j in range(self.size) if self[i][j] is None]

        if greedy:
            def sort_key(item):
                return len(self.get_valid_numbers(item[0], item[1]))

            cells.sort(key=sort_key)

        self.cell_order = cells

    def fill(self, fill_chance):
        """
        Randomly fills the Sudoku board based on the given fill chance.
        Ensures that the board remains valid during the process.
        """
        self.clear()

        self.generate_cell_order()

        self.solve(random_fill=True)

        self.board = [[cell if random() < fill_chance else None for cell in row] for row in self]

    def clear(self, value=None):
        """
        Sets all cells to value which is None by default.
        """
        self.board = [[value for _ in range(self.size)] for _ in range(self.size)]

    def __repr__(self):
        cell_width = ceil(log10(self.size + 1))

        return "\n".join(''.join(f"{(self[i][j] or '')}".rjust(cell_width, '*')
                     for j in range(self.size)) for i in range(self.size)) + "\n"

def get_closest_grid(size: int) -> int:
    """
    Gets the closest rectangle width to a square.
    """
    size_sqrt = size**0.5

    for i in range(int(size_sqrt), size):
        if size//i == size/i:
            return max(i, size//i)

    return 1

def sudoku_from_file(file_name: str) -> Sudoku:
    """
    Reads a sudoku board from a file seperated by lines and commas.
    """
    with open(file_name, "r", encoding="utf-8") as file:
        board = []

        for line in file:
            board.append([])
            for num in line.strip().split(","):
                board[-1].append(int(num) if num.isnumeric() else None)

    return Sudoku(board)

def test_sudoku(sizes: list[int], iters: int, fill_chances: list[int]):
    """
    Tests the sudoku algorithms for the different sizes and fill_chances for iters times.
    """
    times = {}

    for size in sizes:
        sudoku = Sudoku(size)
        times[size] = {}

        for fill in fill_chances:
            times[size][fill] = []

            for _ in range(iters):
                print(size, fill, _)
                sudoku.fill(fill)
                board_keep = deepcopy(sudoku.board)

                sudoku.generate_cell_order()
                start = time.time()
                sudoku.solve()
                end = time.time()-start

                times[size][fill].append(("backtracking", board_keep, end))

                sudoku.board = deepcopy(board_keep)

                sudoku.generate_cell_order()
                start = time.time()
                sudoku.solve(greedy=True)
                end = time.time()-start

                times[size][fill].append(("greedy", board_keep, end))

    return times


if __name__ == "__main__":
    s = Sudoku(9)
    s.fill(0.1)
    print(s)
