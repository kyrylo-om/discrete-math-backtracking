import tkinter as tk
from tkinter import ttk
from time import sleep

class SudokuVis:
    def __init__(self, master):
        self.master = master
        self.master.configure(bg="#333")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Cell.TEntry",
                        foreground="white",
                        fieldbackground="#333",
                        background="#333")

        style.configure("PreSolved.TEntry",
                        foreground="#bbb",
                        fieldbackground="#333",
                        background="#333")


        style.configure("TLabel",
                        foreground="white",
                        fieldbackground="#white",
                        background="#333")

        self.master.title("Sudoku Visualization")

        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.build_grid()

        self.solve_button = tk.Button(master, text="Solve", command=self.solve)
        self.solve_button.grid(row=9, column=0, columnspan=4, sticky="we")

        self.clear_button = tk.Button(master, text="Clear", command=self.clear)
        self.clear_button.grid(row=9, column=5, columnspan=4, sticky="we")

        self.slider_label = ttk.Label(self.master, text="Delay (seconds)")
        self.slider_label.grid(row=10, column=0, columnspan=9, sticky="we")

        self.sleep_slider = tk.Scale(master, from_=0.0, to=1.0, resolution=0.001, orient=tk.HORIZONTAL)
        self.sleep_slider.grid(row=11, column=0, columnspan=9, sticky="we")

        self.solving = False

        self.sudoku = None

    def build_grid(self):
        for i in range(9):
            for j in range(9):
                entry = ttk.Entry(self.master, style="Cell.TEntry", width=2, font=("Arial", 40), justify="center")
                entry.grid(row=i, column=j, padx=(0 if j % 3 else 8, 0), pady=(0 if i % 3 else 8, 0), ipady=4, ipadx=4)
                entry.bind("<KeyPress>", lambda e, x=i, y=j: self.on_key(e, x, y))
                self.entries[i][j] = entry

    def on_key(self, event, i, j):
        char = event.char

        arrow_dict = {"Right": [0, 1], "Left": [0, -1], "Up": [-1, 0], "Down": [1, 0]}

        if event.keysym in arrow_dict:
            a, b = arrow_dict[event.keysym]

            if 0 <= i+a <= 8 and 0 <= j+b <= 8:
                self.entries[i+a][j+b].focus()
            return None

        if self.solving:
            return "break"

        if event.keysym == "BackSpace":
            self.entries[i][j].delete(0, tk.END)
            return None

        if char.isdigit() and 1 <= int(char) <= 9:
            self.entries[i][j].delete(0, tk.END)
            self.entries[i][j].insert(0, char)

        return "break"

    def read_board(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get()
                row.append(int(val) if val else None)
            board.append(row)
        return board

    def update_cell(self, i, j, value):
        sleep(self.sleep_slider.get())

        cell = self.entries[i][j]

        cell.delete(0, tk.END)

        if value != "":
            cell.insert(0, str(value))

        self.master.update()

    def solve(self):
        board = self.read_board()

        self.sudoku = Sudoku(board)

        if self.sudoku.is_board_valid():
            for i in range(9):
                for j in range(9):
                    if self.entries[i][j].get():
                        self.entries[i][j].configure(style="PreSolved.TEntry")

            self.solving = True

            self.sudoku.generate_cell_order()

            try:
                self.sudoku.solve(self)
            except StopIteration:
                self.clear()

            for i in range(9):
                for j in range(9):
                    self.entries[i][j].configure(style="Cell.TEntry")

            self.solving = False

        else:
            print("Invalid Board.")

    def clear(self):
        if self.sudoku is None:
            return

        self.sudoku.stop_solve = True

        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)


class Sudoku:
    def __init__(self, board):
        self.board = board

        self.cell_order = []

        self.stop_solve = False

        self.generate_cell_order()

    def is_move_valid(self, row, col, num):
        for i in range(9):
            if num in (self.board[row][i], self.board[i][col]):
                return False

        start_row = row // 3 * 3
        start_col = col // 3 * 3

        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False
        return True

    def find_next_cell(self):
        for cell in self.cell_order:
            if self.board[cell[0]][cell[1]] is None:
                return cell

        return None

    def solve(self, visualization: SudokuVis | None=None):
        if self.stop_solve:
            self.stop_solve = False
            raise StopIteration

        cell = self.find_next_cell()

        if cell is None:
            return True

        row, col = cell

        for num in range(1, 10):
            if self.is_move_valid(row, col, num):
                self.board[row][col] = num

                if visualization:
                    visualization.update_cell(row, col, num)

                if self.solve(visualization):
                    return True

                self.board[row][col] = None

                if visualization:
                    visualization.update_cell(row, col, "")

        return False

    def is_board_valid(self):
        rows = {i: set() for i in range(9)}
        columns = {i: set() for i in range(9)}

        for i in range(9):
            for j in range(9):
                cell = self.board[i][j]
                if cell is None:
                    continue

                if cell in rows[i]:
                    return False

                rows[i].add(cell)

                if cell in columns[j]:
                    return False

                columns[j].add(cell)

        for a in range(3):
            for b in range(3):
                grid = set()

                for i in range(3):
                    for j in range(3):
                        cell = self.board[a*3+i][b*3+j]

                        if cell is None:
                            continue

                        if cell in grid:
                            return False

                        grid.add(cell)

        return True

    def generate_cell_order(self):
        cells = [(i,j) for i in range(9) for j in range(9) if self.board[i][j] is None]

        def sort_key(item):
            i, j = item

            count = 0

            for num in range(1, 10):
                if not self.is_move_valid(i, j, num):
                    count += 1

            return count

        cells.sort(key=sort_key, reverse=True)

        self.cell_order = cells


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuVis(root)
    root.mainloop()
