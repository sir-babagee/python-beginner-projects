
def find_next_empty(puzzle):
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == -1:
                return r, c

    return None, None  # if no spaces in the puzzle are empty (-1)


def is_valid(puzzle, guess, row, col):
    # figures out whether a guess at the row/col of the puzzle is valid
    # returns True if valid, False otherwise

    # let's start with the row:
    row_vals = puzzle[row]
    if guess in row_vals:
        return False

    # now the columns
    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False

    # and then the square
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3

    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:
                return False

    # if we get here, these checks pass
    return True


def solve_sudoku(puzzle):
    # solve sudoku using a backtracking technique

    row, col = find_next_empty(puzzle)

    if row is None:
        return True

    # if there is a place to put a number, then make a guess between 1 and 9
    for guess in range(1, 10):
        if is_valid(puzzle, guess, row, col):
            # if this is valid, then place guess at that row/col
            puzzle[row][col] = guess
            # now recurse using this puzzle
            # recursively call our function
            if solve_sudoku(puzzle):
                return True

        # if not valid OR if our guess does not solve the puzzle
        # then we need to backtrack and try a new number
        puzzle[row][col] = -1  # reset the guess

    # if none of the numbers that we try work, then this puzzle is UNSOLVABLE
    return False


if __name__ == '__main__':
    example_board = [
        [3, 9, -1,   -1, 5, -1,    -1, -1, -1],
        [-1, -1, -1,   2, -1, -1,    -1, -1, 5],
        [-1, -1, -1,   7, 1, 9,    -1, 8, -1],

        [-1, 5, -1,   -1, 6, 8,    -1, -1, -1],
        [2, -1, 6,   -1, -1, 3,    -1, -1, -1],
        [-1, -1, -1,   -1, -1, -1,    -1, -1, 4],

        [5, -1, -1,   -1, -1, -1,    -1, -1, -1],
        [6, 7, -1,   1, -1, 5,    -1, 4, -1],
        [1, -1, 9,   -1, -1, -1,    2, -1, -1],
    ]

    print(solve_sudoku(example_board))
    print(example_board)
