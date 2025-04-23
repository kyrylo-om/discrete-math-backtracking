maze_map = [
    ["A", 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, "B"],
]

MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def find_all_paths(maze, solution=None, start=None, final=None):
    """
    finds all paths in the maze
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
                final.append(solution + ["B"])
            elif cell == 0:
                maze[start[0]][start[1]] = 1
                solution.append((point[0], point[1]))
                find_all_paths(maze, solution, point, final)
                solution.pop()
                maze[start[0]][start[1]] = 0
    return final


def shortest_path(lst):
    """
    finds the shortest path
    """
    d = dict()
    for e in lst:
        d.setdefault(len(e), e)
    return d.get(min(d))
