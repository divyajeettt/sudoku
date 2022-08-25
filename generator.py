import random


"""
generate a random sudoku board and sort it to be Sudoku - Valid using
Shrinking Square Algorithm*

STEP 1: Box and Adjacent Cell Swap (BAS)
STEP 2: Preferred Adjacent Cell Swap (PAS)
STEP 3: Advance and Backtrack Sort (ABS)

Formulae:

i in range(81):
    # Per Box Formula
    # BOARD[((i // 3) % 3) * 9 + ((i % 27) // 9) * 3 + (i // 27) * 27 + (i % 3)]

    # Box Origin Formula
    # BOARD[((i % 9) // 3) * 3 + (i // 27) * 27]

    # Row Origin Formula
    # BOARD[(i // 9) * 9]

    # Column Origin Formula
    # BOARD[i % 9]

i in range(9):
    # Box Origin Formula
    # BOARD[(i * 3) % 9 + ((i * 3) // 9) * 27]

    # Row Origin Formula
    # BOARD[i * 9]

    # Column Origin Formula
    # BOARD[i]

    # Box Step Formula
    # box_origin + (i // 3) * 9 + (i % 3)

    # Row Step Formula
    # row_origin + i

    # Column Step Formula
    # col_origin + i*9
"""


def make_board():
    """returns a pre-cursor to the Sudoku Board - a 1D list of 81 numbers
    with unique numbers from 1 - 9 in each Box"""

    numbers = []
    for _ in range(9):
        numbers.extend(random.sample(range(1, 10), 9))

    board = [0 for _ in range(81)]
    for k in range(81):
        index = ((k // 3) % 3) * 9 + ((k % 27) // 9) * 3 + (k // 27) * 27 + (k % 3)
        board[index] = numbers[k]

    return board


def grid():
    """returns a VALID Sudoku Board as a nested 2D Grid / List"""

    board = make_board()

    # tracks all rows and columns that have been sorted
    SORTED = [False for _ in range(9) for _ in range(9)]

    for i in range(9):
        backtrack = False

        # 0 is row, 1 is column
        for track in range(2):
            tracker = ((track % 2) == 0)

            registered = [False for _ in range(10)]
            # index 0 will intentionally be left empty since numbers are 1 - 9

            row_origin, col_origin = i*9, i

            for j in range(9):
                # loop label: ROW_COL
                break_ROW_COL = continue_ROW_COL = False

                # row / column stepping
                # ensure that numbers are only registered once marking which cells have been sorted

                step = (row_origin + j) if tracker else (col_origin + j*9)
                num = board[step]

                if not registered[num]:
                    registered[num] = True
                else:
                    # if duplicate in row / column: Box and Adjacent-Cell Swap (BAS)
                    # check for unregistered and unsorted options in same Box
                    # or unregistered and sorted options in the adjacent cells

                    for y in range(j, -1, -1):
                        scan = i*9 + y if tracker else y*9 + i

                        if board[scan] == num:
                            # box stepping

                            start = (i%3 + 1) * 3 if tracker else 0
                            for z in range(start, 9):
                                if (not tracker) and (z%3 <= i%3):
                                    continue

                                box_origin = (scan%9 // 3) * 3 + (scan//27) * 27
                                box_step = box_origin + (z // 3) * 9 + (z % 3)
                                box_num = board[box_step]

                                conds1 = {
                                    not SORTED[scan], not SORTED[box_step], not registered[box_num]
                                }
                                conds2 = {
                                    SORTED[scan], not registered[box_num],
                                    (box_step%9 == scan%9 if tracker else box_step//9 == scan//9)
                                }

                                if all(conds1) or all(conds2):
                                    board[scan], board[box_step] = box_num, num
                                    registered[box_num] = True
                                    continue_ROW_COL = True

                                elif z == 8:
                                    # break statement not reached: no options available
                                    # Preferred Adjacent Cell Swap (PAS)
                                    # swap x with y (preference on unregistered numbers)
                                    # find occurence of y and swap with z, ...
                                    # until an unregistered number has been found

                                    search_no = num
                                    blindswap = [False for _ in range(81)]

                                    # max 18 swaps are possible so this loop runs 18 times at max
                                    for q in range(18):
                                        for b in range(j + 1):
                                            # loop label: SWAP
                                            break_SWAP = False

                                            pace = row_origin + b if tracker else col_origin + b*9

                                            if board[pace] == search_no:
                                                adj_cell = adj_no = -1
                                                decrement = 9 if tracker else 1

                                                for c in range(1, 3 - i%3):
                                                    adj_cell = pace + ((c+1)*9 if tracker else c+1)

                                                    conds3 = {tracker, adj_cell >= 81}
                                                    conds4 = {not tracker, (adj_cell % 9 == 0)}

                                                    if all(conds3) or all(conds4):
                                                        adj_cell -= decrement
                                                    else:
                                                        adj_no = board[adj_cell]
                                                        conds5 = {
                                                            i%3 != 0, c != 1, blindswap[adj_cell],
                                                            registered[adj_no]
                                                        }
                                                        if any(conds5):
                                                            adj_cell -= decrement

                                                    adj_no = board[adj_cell]

                                                    # if it hasn't been swapped before, swap it
                                                    if not blindswap[adj_cell]:
                                                        blindswap[adj_cell] = True
                                                        board[pace] = adj_no
                                                        board[adj_cell] = search_no
                                                        search_no = adj_no

                                                        if not registered[adj_no]:
                                                            registered[adj_no] = True
                                                            continue_ROW_COL = True

                                                        break_SWAP = True

                                                    if break_SWAP or continue_ROW_COL:
                                                        break

                                            if break_SWAP or continue_ROW_COL:
                                                break

                                    if not any({break_ROW_COL, continue_ROW_COL, break_SWAP}):
                                        # if continue or break statements are not reached: fail-safe
                                        # begin Advance and Backtrack Sort (ABS)
                                        # continue to sort next row and column and come back
                                        backtrack = True
                                        break_ROW_COL = True

                                if break_ROW_COL or continue_ROW_COL:
                                    break

                        if break_ROW_COL or continue_ROW_COL:
                            break

                if break_ROW_COL:
                    break

            if tracker:
                # setting row as sorted
                for j in range(9):
                    SORTED[i*9 + j] = True
            elif not backtrack:
                # setting column as sorted
                for j in range(9):
                    SORTED[i + j*9] = True
            else:
                # resetting sorted cells through to the last iteration
                backtrack = False
                for j in range(9):
                    SORTED[i*9 + j] = False
                    SORTED[(i-1)*9 + j] = False
                    SORTED[i-1 + j*9] = False
                i -= 2

    board2D = [[board.pop(0) for y in range(9)] for x in range(9)]

    return board2D if valid(board2D) else grid()


def valid(matrix):
    """returns True if the 2D matrix generated is VALID according to Sudoku rules and
    False in all other cases (repitition of numbers in Row, Column or Sector / Box"""

    for i in range(9):
        row, col = set(), set()
        for j in range(9):
            row.add(matrix[i][j])
            col.add(matrix[j][i])
        if row != col:
            return False

    for range1 in (range(3), range(3, 6), range(6, 9)):
        for range2 in (range(3), range(3, 6), range(6, 9)):
            box = set(matrix[j][i] for i in range1 for j in range2)
            if box != set(range(1, 10)):
                return False

    return True
