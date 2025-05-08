import tkinter as tk
import copy
from collections import deque

CELL_SIZE = 50
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

maze_map = [
    ["A", 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, "B"],
]


def find_all_paths(maze, solution=None, start=None, final=None):
    if solution is None:
        solution = []
    if start is None:
        start = []
    if final is None:
        final = []

    if not start:
        for k, i in enumerate(maze):
            for g, e in enumerate(i):
                if e == "A":
                    start = [k, g]
                    break
            if start:
                break

    row = len(maze)
    col = len(maze[0])

    for move in MOVES:
        point = [start[0] + move[0], start[1] + move[1]]

        if 0 <= point[0] < row and 0 <= point[1] < col:
            cell = maze[point[0]][point[1]]

            if cell == 1:
                continue
            elif cell == "B":
                final.append(solution + [(point[0], point[1])])
            elif cell == 0:
                maze_copy = copy.deepcopy(maze)
                maze_copy[start[0]][start[1]] = 1
                new_solution = solution + [(point[0], point[1])]
                find_all_paths(maze_copy, new_solution, point, final)
    return final


class MazeVisualizer:
    def __init__(self, maze):
        self.maze = maze
        self.path_steps = []

        self.root = tk.Tk()
        self.root.title("Maze Path Backtracking")

        self.canvas = tk.Canvas(
            self.root, width=len(maze[0]) * CELL_SIZE, height=len(maze) * CELL_SIZE
        )
        self.canvas.grid(row=0, column=0, columnspan=2)

        control_frame = tk.Frame(self.root)
        control_frame.grid(row=1, column=0, columnspan=2, sticky="w")

        self.edit_mode = tk.StringVar(value="wall")
        modes = [
            ("Start (A)", "A"),
            ("Exit (B)", "B"),
            ("Wall", "wall"),
            ("Erase", "erase"),
        ]
        for text, mode in modes:
            tk.Radiobutton(
                control_frame, text=text, variable=self.edit_mode, value=mode
            ).pack(side="left", padx=5)

        tk.Button(
            control_frame, text="Start Analysis", command=self.start_analysis
        ).pack(side="left", padx=10)

        self.speed_slider = tk.Scale(
            self.root, from_=0, to=1000, label="Speed (ms)", orient=tk.HORIZONTAL
        )
        self.speed_slider.set(300)
        self.speed_slider.grid(row=2, column=0, columnspan=2, sticky="we")

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.draw_maze()
        self.root.mainloop()

    def on_canvas_click(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE

        if row < 0 or row >= len(self.maze) or col < 0 or col >= len(self.maze[0]):
            return

        mode = self.edit_mode.get()

        if mode == "A":
            for r in range(len(self.maze)):
                for c in range(len(self.maze[r])):
                    if self.maze[r][c] == "A":
                        self.maze[r][c] = 0
            self.maze[row][col] = "A"

        elif mode == "B":
            for r in range(len(self.maze)):
                for c in range(len(self.maze[r])):
                    if self.maze[r][c] == "B":
                        self.maze[r][c] = 0
            self.maze[row][col] = "B"

        elif mode == "wall":
            if self.maze[row][col] not in ("A", "B"):
                self.maze[row][col] = 1

        elif mode == "erase":
            if self.maze[row][col] not in ("A", "B"):
                self.maze[row][col] = 0

        self.draw_maze()

    def draw_maze(self, path=None, color="red"):
        self.canvas.delete("all")
        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                x1 = j * CELL_SIZE
                y1 = i * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                fill = "#babdc2"
                if cell == 1:
                    fill = "black"
                elif cell == "A":
                    fill = "green"
                elif cell == "B":
                    fill = "blue"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="gray")

        if path:
            for i, j in path:
                x1 = j * CELL_SIZE
                y1 = i * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def prepare_visual_steps(self):
        self.visual_maze = copy.deepcopy(self.maze)
        self.steps = []

        def tracer(maze, solution=None, start=None, final=None):
            if solution is None:
                solution = []
            if start is None:
                start = []
            if final is None:
                final = []

            if not start:
                for k, i in enumerate(maze):
                    for g, e in enumerate(i):
                        if e == "A":
                            start = [k, g]
                            break
                    if start:
                        break

            row = len(maze)
            col = len(maze[0])

            for move in MOVES:
                point = [start[0] + move[0], start[1] + move[1]]

                if 0 <= point[0] < row and 0 <= point[1] < col:
                    cell = maze[point[0]][point[1]]

                    if cell == 1:
                        continue
                    elif cell == "B":
                        path = solution + [(point[0], point[1])]
                        self.steps.append(("final", copy.deepcopy(path)))
                        final.append(path)
                    elif cell == 0:
                        maze_copy = copy.deepcopy(maze)
                        maze_copy[start[0]][start[1]] = 1
                        new_solution = solution + [(point[0], point[1])]
                        self.steps.append(("step", copy.deepcopy(new_solution)))
                        tracer(maze_copy, new_solution, point, final)

        tracer(copy.deepcopy(self.visual_maze))

    def start_analysis(self):
        self.prepare_visual_steps()
        self.animate()

    def animate(self, step=0):
        if step < len(self.steps):
            kind, path = self.steps[step]
            color = "green" if kind == "final" else "red"
            self.draw_maze(path=path, color=color)
            self.root.after(self.speed_slider.get(), self.animate, step + 1)
        else:
            final_paths = [path for kind, path in self.steps if kind == "final"]
            if final_paths:
                shortest_path = min(final_paths, key=lambda x: len(x))
                self.draw_maze(path=shortest_path, color="green")
            else:
                self.canvas.create_text(
                    self.canvas.winfo_width() // 2,
                    self.canvas.winfo_height() // 2,
                    text="No Path Found!",
                    fill="red",
                    font=("Arial", 20, "bold"),)


if __name__ == "__main__":
    MazeVisualizer(maze_map)
