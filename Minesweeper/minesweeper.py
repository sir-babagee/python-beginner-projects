import random
import re

# let's create a board object to represent the minesweeper game
# this is so that we can just say 'create new board object', or
# 'dig here', or 'render this game for this object'


class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # lets create the board
        # helper function
        self.board = self.make_new_board()  # plant the bombs
        self.assign_values_to_board()

        # intialize a set to keep track of which of the locations we've uncovered
        # we'll save (row, col) tuples into this set
        self.dug = set()  # if we dig at 0, 0, then self.dug = {(0, 0)}

    def make_new_board(self):
        # construct new board based on the dim size and num bombs
        # we should construct the list here (or whatever representation you prefer,
        # but since we have a 2-D board, list of lists is most natural)

        # generate a new board
        board = [[None for _ in range(self.dim_size)]
                 for _ in range(self.dim_size)]

        # plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == '*':
                # this means that we've actually planted a bomb there already and we should keep going
                continue

            board[row][col] = '*'
            bombs_planted += 1
        return board

    def assign_values_to_board(self):
        # now that we have the bombs planted, let's assign a number 0-8 for all the empty spaces, which
        # represents how many neighboring bombs there are. We can precompute these and it'll save us some
        # effort checking what's around the board later on :)
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    # if this is already a bomb, we don't want to calculate anything
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        # lets iterate through each of the neighboring positions and sum number of bombs
        # make sure not to go out of bounds
        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size - 1, (row+1)+1)):
            for c in range(max(0, col-1), min(self.dim_size - 1, (col+1)+1)):
                if r == row and c == col:
                    # our original location
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def dig(self, row, col):
        # dig at specific location
        # return True if successful dig, False if bomb dug

        self.dug.add((row, col))  # keep track that we dug
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        for r in range(max(0, row-1), min(self.dim_size - 1, (row+1)+1)):
            for c in range(max(0, col-1), min(self.dim_size - 1, (col+1)+1)):
                if (r, c) in self.dug:
                    # don't dig where you've already dug
                    continue
                self.dig(r, c)

        return True

    def __str__(self):
        # this is a magic function where if you call print on this object,
        # it'll print out what this function returns!
        # return the string that shows the board to the player
        visible_board = [[None for _ in range(
            self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if self.board[row][col] in self.dug:
                    visible_board = str(self.board[row][col])
                else:
                    visible_board = ' '

        # put this together in a string
        string_rep = ''
        #  get max columns for printing
        widths = []
        print(visible_board)
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(len(max(columns, key=len)))

        # printing the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' \n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


# play the game
def play(dim_size=10, num_bombs=10):
    # step 1: create the board and plant the bomb
    board = Board(dim_size, num_bombs)

    # step 2: show the user the board and ask for where to dig
    # step 3a: if location is bomb, show gameover message
    # step 3b: if location is not a bomb, dig recursively until each square each square is at least
    #          next to a bomb
    # step 4: repeat steps 2 and 3a/b until there are no more places to dig -> VICTORY
    safe = True
    while len(board.dug) < board.dim_size**2 - num_bombs:
        print(board)
        user_input = re.split(
            ',(\\s)*', input("Where would like to dig? Input as row, col: "))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size:
            print("Invalid location. Try again")
            continue

        # if it's valid, we dig
        safe = board.dig(row, col)
        if not safe:
            # dug a bomb
            break  # game over

    if safe:
        print("Congratulations, you are victorious".upper())
    else:
        print('SORRY, GAME OVER')
        # let's reveal the whole board
        board.dug = [(r, c) for r in range(board.dim_size)
                     for c in range(board.dim_size)]
        print(board)


if __name__ == "__main__":
    play()
