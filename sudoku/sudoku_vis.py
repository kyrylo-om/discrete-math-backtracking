"""
Sudoku visualization 
"""

import tkinter as tk
from tkinter import ttk
from time import sleep
from math import log10, ceil
from sudoku_cls import Sudoku, get_closest_grid

class UserAbortedError(Exception):
    """Error for exiting out of sudoku visualization."""

class SudokuVis:
    """
    Sudoku visualization class.
    """
    def __init__(self, master, board):
        if isinstance(board, int):
            size = board
            if size > 49:
                confirm = input("Warning: high values for board size are not recommended .\n"
                                f"Are you sure you want to create a {size}x{size} sudoku? (y/n): ")

                if confirm == "n":
                    raise UserAbortedError

            self.size = size
        elif isinstance(board, list):
            self.size = len(board)

            if any(self.size != len(row) for row in board):
                raise ValueError("Board width and height should be the same.")

        if isinstance(board, Sudoku):
            self.grid_width = board.grid_width
            self.grid_height = board.grid_width
            self.size = board.size

            board = board.board
        else:
            self.grid_width = get_closest_grid(self.size)
            self.grid_height = self.size//self.grid_width

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

        if isinstance(board, list):
            self.entries = board
        else:
            self.entries = [[None for _ in range(self.size)] for _ in range(self.size)]

        self.build_grid()

        self.solve_button = tk.Button(master, text="Solve", command=self.solve)
        self.solve_button.grid(row=self.size, column=0, columnspan=self.size//2, sticky="we")

        self.solve_greedy_button = tk.Button(master, text="Solve Greedy", command=lambda: self.solve(greedy=True))
        self.solve_greedy_button.grid(row=self.size+1, column=0, columnspan=self.size//2,
                                      sticky="we")

        self.clear_button = tk.Button(master, text="Clear", command=self.clear)
        self.clear_button.grid(row=self.size, column=ceil(self.size/2),
                               columnspan=self.size//2, sticky="we")

        self.clear_placed_button = tk.Button(master, text="Clear Placed", command=self.clear_placed)
        self.clear_placed_button.grid(row=self.size+1, column=ceil(self.size/2),
                                      columnspan=self.size//2, sticky="we")

        self.sleep_slider_label = ttk.Label(self.master, text="Delay (seconds)")
        self.sleep_slider_label.grid(row=self.size+2, column=0, columnspan=self.size, sticky="we")

        self.sleep_slider = tk.Scale(master, from_=0.0, to=1.0, resolution=0.001, orient=tk.HORIZONTAL)
        self.sleep_slider.grid(row=self.size+3, column=0, columnspan=self.size, sticky="we")

        self.visualize_solve_button = tk.Button(master, text="Visualization: ON", command=self.toggle_visualize)
        self.visualize_solve_button.grid(row=self.size+4, column=0, columnspan=self.size, sticky="we")

        self.fill_slider_label = ttk.Label(self.master, text="Fill chance")
        self.fill_slider_label.grid(row=self.size+5, column=0, columnspan=self.size, sticky="we")

        self.fill_slider = tk.Scale(master, from_=0.0, to=1.0, resolution=0.001, orient=tk.HORIZONTAL)
        self.fill_slider.set(0.5)
        self.fill_slider.grid(row=self.size+6, column=0, columnspan=self.size, sticky="we")

        self.fill_button = tk.Button(master, text="Randomly fill board", command=self.fill)
        self.fill_button.grid(row=self.size+7, column=0, columnspan=self.size, sticky="we")

        self.visualize = True
        self.solving = False
        self.sudoku = None

    def build_grid(self):
        """
        Builds the entries grid of tkinter entry components for displaying a sudoku board.
        """
        for i in range(self.size):
            for j in range(self.size):
                entry = ttk.Entry(self.master, style="Cell.TEntry", width=int(log10(self.size)+1),
                                   font=("Arial", 400//self.size), justify="center")

                entry.grid(row=i, column=j, padx=(0 if j % self.grid_width else 8, 0),
                            pady=(0 if i % self.grid_height else 8, 0), ipady=0, ipadx=100//self.size)

                entry.bind("<KeyPress>", lambda e, x=i, y=j: self.on_key(e, x, y))

                if self.entries[i][j] is not None:
                    entry.insert(0, str(self.entries[i][j]))

                    entry.configure(style="PreSolved.TEntry")

                self.entries[i][j] = entry

    def on_key(self, event, i, j):
        """
        Handles keyboard inputs on the visualized board.
        """
        char = event.char

        arrow_dict = {"Right": [0, 1], "Left": [0, -1], "Up": [-1, 0], "Down": [1, 0]}

        if event.keysym in arrow_dict:
            a, b = arrow_dict[event.keysym]

            if 0 <= i+a <= self.size-1 and 0 <= j+b <= self.size-1:
                self.entries[i+a][j+b].focus()
            return None

        if self.solving:
            return "break"

        if event.keysym == "BackSpace":
            self.entries[i][j].delete(0, tk.END)

            return "break"

        if char.isdigit():
            new_num = str(int(self.entries[i][j].get() + char) % 10**int(log10(self.size)+1))

            self.entries[i][j].delete(0, tk.END)
            self.entries[i][j].insert(0, new_num)

        return "break"

    def read_board(self):
        """
        Constructs a board from the entries list.
        """
        return [[int(self.entries[j][i].get() or 0) or None for i in range(self.size)]
                                                            for j in range(self.size)]
    def write_board(self, board):
        """
        Constructs a board from the entries list.
        """
        for i in range(self.size):
            for j in range(self.size):
                self.entries[i][j].delete(0, tk.END)

                self.entries[i][j].insert(0, str(board[i][j] or ""))

    def update_cell(self, i, j, value):
        """
        Method for updating cell values during solving.
        """
        sleep_amount = self.sleep_slider.get()
        if sleep_amount:
            sleep(sleep_amount)

        cell = self.entries[i][j]

        cell.delete(0, tk.END)
        if value != "":
            cell.insert(0, str(value))

        self.master.update()

    def solve(self, greedy=False):
        """
        Converts the entires 2D list into an int 2D list and Solves it using the Sudoku class.
        """
        if self.solving:
            return

        board = self.read_board()

        self.sudoku = Sudoku(board)

        if self.sudoku.find_next_cell() is None:
            return

        if self.sudoku.is_board_valid():
            for i in range(self.size):
                for j in range(self.size):
                    if self.entries[i][j].get():
                        self.entries[i][j].configure(style="PreSolved.TEntry")
                    else:
                        self.entries[i][j].configure(style="Cell.TEntry")

            self.solving = True

            self.sudoku.generate_cell_order()

            if self.visualize:
                try:
                    self.sudoku.solve(visualization=self, greedy=greedy)
                except StopIteration:
                    self.clear_placed()
            else:
                try:
                    self.sudoku.solve(greedy=greedy)
                    self.write_board(self.sudoku.board)
                except StopIteration:
                    self.clear_placed()

            self.solving = False

        else:
            print("Invalid Board.")

    def clear(self):
        """
        Clears all entries to tk.END.
        """
        if self.sudoku is None:
            return

        self.sudoku.stop_solve = True

        for i in range(self.size):
            for j in range(self.size):
                self.entries[i][j].delete(0, tk.END)

    def clear_placed(self):
        """
        Clears all new placed entries to tk.END.
        """
        if self.sudoku is None:
            return

        self.sudoku.stop_solve = True

        for i in range(self.size):
            for j in range(self.size):
                if self.entries[i][j].cget("style") != "PreSolved.TEntry":
                    self.entries[i][j].delete(0, tk.END)

    def toggle_visualize(self):
        """
        Toggles wether to show visualization or to only show the final result.
        """
        self.visualize = not self.visualize
        self.visualize_solve_button.config(
            text=f"Visualization: {"ON (Slower)" if self.visualize else "OFF (Faster)"}")

    def fill(self):
        """
        Fills the board using the base sudoku class fill method and displays it on screen.
        """
        for i in range(self.size):
            for j in range(self.size):
                self.entries[i][j].configure(style="Cell.TEntry")

        sudoku = Sudoku(self.size)

        sudoku.fill(self.fill_slider.get())

        self.write_board(sudoku.board)

def init_visualization(board):
    root = tk.Tk()
    try:
        app = SudokuVis(root, board)
    except UserAbortedError:
        print("Exitting out of application.")
    else:
        root.mainloop()

    return app

if __name__ == "__main__":
    init_visualization(9)
