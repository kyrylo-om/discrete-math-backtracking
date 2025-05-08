import tkinter as tk
import time
from tkinter import messagebox

CELL_SIZE = 50


def generate_board(queens, length, width):
    board = [[0 for _ in range(width)] for _ in range(length)]
    for i, j in queens:
        board[i][j] = "Q"
    for i, j in queens:
        for a in range(width):
            if board[i][a] == 0:
                board[i][a] = 1
        for a in range(length):
            if board[a][j] == 0:
                board[a][j] = 1
        d = i - j
        for x in range(length):
            y = x - d
            if 0 <= y < width and board[x][y] == 0:
                board[x][y] = 1
        s = i + j
        for x in range(length):
            y = s - x
            if 0 <= y < width and board[x][y] == 0:
                board[x][y] = 1
    return board


def find_all_queens(n,length,width,queens=None,rows=None,cols=None,diag1=None,diag2=None,start_pos=0,callback=None,delay=0,final=None):
    if queens is None:
        queens = []
    if rows is None:
        rows = [0] * length
    if cols is None:
        cols = [0] * width
    if diag1 is None:
        diag1 = [0] * (length + width - 1)
    if diag2 is None:
        diag2 = [0] * (length + width - 1)
    if final is None:
        final = []

    current_count = len(queens)
    if current_count > n:
        return final
    if current_count == n:
        if callback:
            board = generate_board(queens, length, width)
            callback(board, highlight="solution")
            time.sleep(delay)
        final.append(generate_board(queens, length, width))
        return final

    for pos in range(start_pos, length * width):
        i, j = divmod(pos, width)
        d1 = i - j + (width - 1)
        d2 = i + j
        if rows[i] == 0 and cols[j] == 0 and diag1[d1] == 0 and diag2[d2] == 0:
            queens.append((i, j))
            rows[i] += 1
            cols[j] += 1
            diag1[d1] += 1
            diag2[d2] += 1

            if callback:
                board = generate_board(queens, length, width)
                callback(board, highlight=[(i, j)])
                time.sleep(delay)

            find_all_queens(n,length,width, queens,rows,cols,diag1,diag2,pos + 1,callback,delay,final,)

            queens.pop()
            rows[i] -= 1
            cols[j] -= 1
            diag1[d1] -= 1
            diag2[d2] -= 1

            if callback:
                board = generate_board(queens, length, width)
                callback(board)
                time.sleep(delay)

    return final


class BacktrackingVisualizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("N-Queens Visualizer")

        self.setup_ui()
        self.root.mainloop()

    def setup_ui(self):
        # Input Frame
        input_frame = tk.Frame(self.root)
        input_frame.grid(row=0, column=0, padx=10, pady=10)

        # Queens input
        tk.Label(input_frame, text="Кількість ферзів:").grid(
            row=0, column=0, sticky="w"
        )
        self.queens_entry = tk.Entry(input_frame)
        self.queens_entry.grid(row=0, column=1, padx=5)

        # Rows input
        tk.Label(input_frame, text="Рядків:").grid(row=1, column=0, sticky="w")
        self.rows_entry = tk.Entry(input_frame)
        self.rows_entry.grid(row=1, column=1, padx=5)

        # Columns input
        tk.Label(input_frame, text="Стовпців:").grid(row=2, column=0, sticky="w")
        self.cols_entry = tk.Entry(input_frame)
        self.cols_entry.grid(row=2, column=1, padx=5)

        # Control buttons
        self.start_btn = tk.Button(
            input_frame, text="Старт", command=self.start_visualization
        )
        self.start_btn.grid(row=3, column=0, columnspan=2, pady=5)

        # Speed control
        self.speed_slider = tk.Scale(
            self.root, from_=0, to=1000, label="Швидкість (мс)", orient=tk.HORIZONTAL
        )
        self.speed_slider.set(500)
        self.speed_slider.grid(row=1, column=0, sticky="we", padx=10)

        # Canvas placeholder (will be recreated on start)
        self.canvas = None

    def validate_inputs(self):
        try:
            n = int(self.queens_entry.get())
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())

            if n <= 0 or rows <= 0 or cols <= 0:
                raise ValueError("Значення мають бути більше 0")

            if n > min(rows, cols):
                raise ValueError(
                    "Неможливо розмістити більше ферзів, ніж мінімальний розмір поля"
                )

            return n, rows, cols

        except ValueError as e:
            messagebox.showerror("Помилка вводу", str(e))
            return None

    def start_visualization(self):
        params = self.validate_inputs()
        if not params:
            return

        n, rows, cols = params

        # Clear previous canvas if exists
        if self.canvas:
            self.canvas.destroy()

        # Create new canvas with proper size
        self.canvas = tk.Canvas(
            self.root, width=cols * CELL_SIZE, height=rows * CELL_SIZE
        )
        self.canvas.grid(row=2, column=0, padx=10, pady=10)

        # Disable inputs during visualization
        self.start_btn.config(state=tk.DISABLED)
        self.queens_entry.config(state=tk.DISABLED)
        self.rows_entry.config(state=tk.DISABLED)
        self.cols_entry.config(state=tk.DISABLED)

        # Start visualization in new thread to keep UI responsive
        self.root.after(100, lambda: self.run_visualization(n, rows, cols))

    def run_visualization(self, n, rows, cols):
        delay = self.speed_slider.get() / 1000
        find_all_queens(n, rows, cols, callback=self.draw_board, delay=delay)
        # Re-enable inputs after completion
        self.start_btn.config(state=tk.NORMAL)
        self.queens_entry.config(state=tk.NORMAL)
        self.rows_entry.config(state=tk.NORMAL)
        self.cols_entry.config(state=tk.NORMAL)

    def draw_board(self, board, highlight=None):
        if not self.canvas:
            return

        self.canvas.delete("all")
        rows = len(board)
        cols = len(board[0]) if rows > 0 else 0

        for i in range(rows):
            for j in range(cols):
                x1 = j * CELL_SIZE
                y1 = i * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                color = "white" if (i + j) % 2 == 0 else "lightgray"
                if highlight == "solution":
                    color = "#90EE90"  # Light green
                elif highlight and (i, j) in highlight:
                    color = "#ADD8E6"  # Light blue

                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color, outline="black"
                )

                if board[i][j] == "Q":
                    self.canvas.create_text(
                        x1 + CELL_SIZE // 2,
                        y1 + CELL_SIZE // 2,
                        text="♛",
                        font=("Arial", CELL_SIZE // 2),
                        fill="red",
                    )
                elif board[i][j] == 1:
                    self.canvas.create_rectangle(
                        x1 + 2, y1 + 2, x2 - 2, y2 - 2, fill="#ffcccc", outline=""
                    )
        self.root.update()
if __name__ == "__main__":
    BacktrackingVisualizer()
