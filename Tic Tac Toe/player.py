import math
import random


class Player:
    def __init__(self, letter):
        #letter is x or o
        self.letter = letter

    # we want players to get their next move

    def get_move(self, game):
        pass


class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-8): ')

            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print("Invalid square. Try again.")

        return val


class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            # choose a random square for the first move
            square = random.choice(game.available_moves())
        else:
            # get the square based off of the minimax algorithm
            square = self.minimax(game, self.letter)['position']

        return square

    def minimax(self, state, player):
        max_player = self.letter  # yourself
        # the other player...so whatever letter you're not
        other_player = 'O' if player == 'X' else 'X'

        # first we have to check if the previous move is a winner
        # this is our base case
        if state.current_winner == other_player:
            # we should return the position AND score because we need to keep trackof the score
            # for the minimax to work
            return {'position': None,
                    'score': 1 * (state.num_of_empty_squares() + 1) if other_player == max_player else -1 * (state.num_of_empty_squares() + 1)
                    }

        elif not state.num_of_empty_squares():  # no empty squares
            return {'position': None, 'score': 0}

        if player == max_player:
            # each score should maximize
            best = {'position': None, 'score': -math.inf}
        else:
            # each score should minimize
            best = {'position': None, 'score': math.inf}

        for possible_move in state.available_moves():
            # step 1: make a move
            state.make_move(possible_move, player)

            # step 2: recurse using minimax to simulate a game after making that move
            # now we alternate player
            sim_score = self.minimax(state, other_player)

            # step 3: undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            # step 4: update the dictionaries if necessary
            if player == max_player:  # we are trying to maximize the max_player
                if sim_score['score'] > best['score']:
                    best = sim_score  # replace best
            else:  # but minimize the other player
                if sim_score['score'] < best['score']:
                    best = sim_score  # replace best

        return best
