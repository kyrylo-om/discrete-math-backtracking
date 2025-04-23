import copy


def mark_attacks(board, i, j, lenth, width):
    """
    marks all ataking spots with 1
    """
    new_board = copy.deepcopy(board)

    for a in range(width):
        if new_board[i][a] != "Q":
            new_board[i][a] = 1
    for a in range(lenth):
        if new_board[a][j] != "Q":
            new_board[a][j] = 1
    
    for d in range(-min(i, j), min(lenth - i, width - j)):
        if new_board[i + d][j + d] != "Q":
            new_board[i + d][j + d] = 1
    for d in range(-min(i, width - j - 1), min(lenth - i, j + 1)):
        if new_board[i + d][j - d] != "Q":
            new_board[i + d][j - d] = 1

    new_board[i][j] = "Q"
    return new_board


def count_queens(board):
    """
    counts how many queens there are
    """
    return sum(cell == "Q" for row in board for cell in row)


def find_all_queens(n, lenth, width, google=None, score=None, final=None, start_pos=0):
    """
    finds all positions for queens
    """
    if not google:
        for _ in range(lenth):
            mid = []
            for _ in range(width):
                mid.append(0)
            google.append(mid)
    if score is None:
        score = []
    if final is None:
        final = []

    if count_queens(google) == n:
        final.append(copy.deepcopy(google))
        return final

    for pos in range(start_pos, lenth * width):
        i, j = divmod(pos, width)
        if google[i][j] == 0:
            new_google = mark_attacks(google, i, j, lenth, width)
            score.append((i, j))
            find_all_queens(n, lenth, width, new_google, score, final, pos + 1)
            score.pop()

    return final
