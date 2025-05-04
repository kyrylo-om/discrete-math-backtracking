import tkinter as tk
import time

CELL_SIZE = 80


def mark_attacks(board, i, j, length, width):
    new_board = [row[:] for row in board]
    for a in range(width):
        if new_board[i][a] != "Q":
            new_board[i][a] = 1
    for a in range(length):
        if new_board[a][j] != "Q":
            new_board[a][j] = 1
    for d in range(-min(i, j), min(length - i, width - j)):
        if new_board[i + d][j + d] != "Q":
            new_board[i + d][j + d] = 1
    for d in range(-min(i, width - j - 1), min(length - i, j + 1)):
        if new_board[i + d][j - d] != "Q":
            new_board[i + d][j - d] = 1
    new_board[i][j] = "Q"
    return new_board


def count_queens(board):
    return sum(cell == "Q" for row in board for cell in row)


def find_all_queens(
    n,
    length,
    width,
    google=None,
    score=None,
    final=None,
    start_pos=0,
    callback=None,
    delay=0.5,
):
    if not google:
        google = [[0 for _ in range(width)] for _ in range(length)]
    if score is None:
        score = []
    if final is None:
        final = []

    current_count = count_queens(google)
    if current_count > n:
        return final
    if current_count == n:
        if callback:
            callback(google, highlight="solution")
            time.sleep(delay)
        final.append([row[:] for row in google])
        return final

    for pos in range(start_pos, length * width):
        i, j = divmod(pos, width)
        if google[i][j] == 0:
            if callback:
                callback(google, highlight=[(i, j)])
                time.sleep(delay)

            new_google = mark_attacks(google, i, j, length, width)
            if callback:
                callback(new_google)
                time.sleep(delay)

            score.append((i, j))
            find_all_queens(
                n, length, width, new_google, score, final, pos + 1, callback, delay
            )
            score.pop()

            if callback:
                callback(google)
                time.sleep(delay)

    return final


class BacktrackingVisualizer:
    def __init__(self, n, length, width):
        self.n = n
        self.length = length
        self.width = width

        self.root = tk.Tk()
        self.root.title("Backtracking Queens")

        self.canvas = tk.Canvas(
            self.root, width=width * CELL_SIZE, height=length * CELL_SIZE
        )
        self.canvas.grid(row=0, column=0, columnspan=2)

        self.speed_slider = tk.Scale(
            self.root, from_=0, to=1000, label="Speed (ms)", orient=tk.HORIZONTAL
        )
        self.speed_slider.set(500)
        self.speed_slider.grid(row=1, column=0, columnspan=2, sticky="we")

        self.root.after(500, self.run_visualization)
        self.root.mainloop()

    def draw_board(self, board, highlight=None):
        self.canvas.delete("all")
        for i in range(self.length):
            for j in range(self.width):
                x1 = j * CELL_SIZE
                y1 = i * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                if highlight == "solution":
                    color = "green"
                elif highlight and (i, j) in highlight:
                    color = "lightblue"
                else:
                    color = "white" if (i + j) % 2 == 0 else "lightgray"

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
                        x1 + 1, y1 + 1, x2 - 1, y2 - 1, fill="#ffcccc", outline=""
                    )
        self.root.update()

    def run_visualization(self):
        delay = self.speed_slider.get() / 1000
        find_all_queens(
            self.n, self.length, self.width, callback=self.draw_board, delay=delay
        )


if __name__ == "__main__":
    BacktrackingVisualizer(n=4, length=4, width=4)
