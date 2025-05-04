import tkinter as tk
import copy

CELL_SIZE = 60
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

maze_map = [
    ["A", 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1],
    [0, 0, 1, 0, 1, 0, 1],
    [0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, "B"],
]


def find_all_paths(maze, solution=None, start=None, final=None):
    """
    Finds all path in the labirinth
    """
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
                maze[start[0]][start[1]] = 1
                solution.append((point[0], point[1]))
                find_all_paths(maze, solution, point, final)
                solution.pop()
                maze[start[0]][start[1]] = 0
    return final


class MazeVisualizer:
    def __init__(self, maze):
        self.maze = maze
        self.path_steps = []
        self.prepare_visual_steps()

        self.root = tk.Tk()
        self.root.title("Maze Path Backtracking")

        self.canvas = tk.Canvas(
            self.root, width=len(maze[0]) * CELL_SIZE, height=len(maze) * CELL_SIZE
        )
        self.canvas.grid(row=0, column=0, columnspan=2)

        self.speed_slider = tk.Scale(
            self.root, from_=0, to=1000, label="Speed (ms)", orient=tk.HORIZONTAL
        )
        self.speed_slider.set(300)
        self.speed_slider.grid(row=1, column=0, columnspan=2, sticky="we")

        self.root.after(100, self.animate)
        self.root.mainloop()

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
                        maze[start[0]][start[1]] = 1
                        solution.append((point[0], point[1]))
                        self.steps.append(("step", copy.deepcopy(solution)))
                        tracer(maze, solution, point, final)
                        solution.pop()
                        self.steps.append(("backtrack", copy.deepcopy(solution)))
                        maze[start[0]][start[1]] = 0

        tracer(copy.deepcopy(self.maze))

    def draw_maze(self, path=None, color="red"):
        self.canvas.delete("all")
        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                x1 = j * CELL_SIZE
                y1 = i * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                if cell == 1:
                    fill_color = "black"
                elif cell == "A":
                    fill_color = "green"
                elif cell == "B":
                    fill_color = "blue"
                else:
                    fill_color = "#babdc2"

                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=fill_color, outline="gray"
                )

        if path:
            for i, j in path:
                x1 = j * CELL_SIZE
                y1 = i * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def animate(self, step=0):
        if step < len(self.steps):
            kind, path = self.steps[step]
            color = "green" if kind == "final" else "red"
            self.draw_maze(path=path, color=color)
            delay = self.speed_slider.get()
            self.root.after(delay, self.animate, step + 1)
        else:
            final_paths = [path for kind, path in self.steps if kind == "final"]
            if final_paths:
                self.draw_maze(path=final_paths[-1], color="green")


if __name__ == "__main__":
    MazeVisualizer(maze_map)
