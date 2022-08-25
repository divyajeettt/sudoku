from itertools import product


"""Solve the Sudoku grid using backtracking algorithm
Time complexity: O(9^(n²))"""


def find_empty(board):
    """returns the indices of empty cells"""

    for i, j in product(range(9), range(9)):
        if board[i][j] is None:
            return (i, j)
    return None


def valid(board, num, indices):
    """returns True if num is a valid entry at the given indices"""

    x, y = indices

    for i in range(9):
        # check row
        if (board[x][i] == num) and (y != i):
            return False

        # check column
        if (board[i][y] == num) and (x != i):
            return False

    # check box
    bx, by = (x // 3) * 3, (y // 3) * 3
    for i, j in product(range(bx, bx+3), range(by, by+3)):
        if (board[i][j] == num) and (i, j) != indices:
            return False

    return True


def solve(board, *funcs):
    """solves the Sudoku Grid"""

    if (indices := find_empty(board)) is None:
        return True
    else:
        x, y = indices

    for num in range(1, 10):
        if valid(board, num, indices):
            funcs[4](indices)
            funcs[5](x, y)
            board[x][y] = num
            for func in funcs[:4]:
                func()

            if solve(board, *funcs):
                return True

            funcs[4](indices)
            funcs[5](x, y)
            board[x][y] = None
            for func in funcs[:4]:
                func()

    return False