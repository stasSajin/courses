"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

EMPTY = 1
PLAYERX = 2
PLAYERO = 3 
DRAW = 4

class TTTBoard:
    """
    Class to represent a Tic-Tac-Toe board.
    """

    def __init__(self, dim, reverse = False, board = None):
        """
        Initialize the TTTBoard object with the given dimension and 
        whether or not the game should be reversed.
        """
        self._board = [[" " for dummy_i in range(dim)] for dummy_j in range(dim)]
        self._dim = dim
        self._reverse = reverse
        self._constants = {EMPTY: " ",
                          PLAYERX: "X",
                          PLAYERO: "O"}
            
    def __str__(self):
        """
        Human readable representation of the board.
        """
        return str(self._board)

    def get_dim(self):
        """
        Return the dimension of the board.
        """
        return self._dim
    
    def square(self, row, col):
        """
        Returns one of the three constants EMPTY, PLAYERX, or PLAYERO 
        that correspond to the contents of the board at position (row, col).
        """
        return self._board[row][col]

    def get_empty_squares(self):
        """
        Return a list of (row, col) tuples for all empty squares
        """
        empty = []
        for row in range(self._dim):
            for col in range(self._dim):
                if self._board[row][col] == self._constants[EMPTY]:
                    empty.append((row, col))
        return empty

    def move(self, row, col, player):
        """
        Place player on the board at position (row, col).
        player should be either the constant PLAYERX or PLAYERO.
        Does nothing if board square is not empty.
        """
        if self._board[row][col] == self._constants[EMPTY]:
            self._board[row][col] = player

    def check_win(self):
        """
        Returns a constant associated with the state of the game
            If PLAYERX wins, returns PLAYERX.
            If PLAYERO wins, returns PLAYERO.
            If game is drawn, returns DRAW.
            If game is in progress, returns None.
        """
        # extract rows
        rows = self._board
        # extract columns
        cols = [[self._board[row][col] for row in range(self._dim)] for col in range(self._dim)]
        # extract diagonals
        diag1 = [self._board[i][i] for i in range(self._dim)]
        diag2 = [row[-i-1] for i,row in enumerate(self._board) ]
        
        print "cols", cols
        lines = rows + cols + [diag1]+ [diag2]
        for line in lines:
            if line.count(PLAYERX) == self._dim:
                if self._reverse:
                    self.switch_player(PLAYERX)
                return PLAYERX
            elif line.count(PLAYERO) == self._dim:
                if self._reverse:
                    self.switch_player(PLAYER0)
                return PLAYERO
        
        # check for draws
        if len(self.get_empty_squares()) == 0:
            return DRAW
        else:
            return None
        
    def clone(self):
        """
        Return a copy of the board.
        """
        return TTTBoard(self._dim, self._reverse, self._board)

    def switch_player(player):
        """
        The function switches player
        """
        if player == PLAYERX:
            return PLAYERO
        else:
            return PLAYERX

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player


def mc_trial(board, player):
    """
    This function takes a current board and the next player to move.
    The function should play a game starting with the given player
    by making random moves, alternating between players.
    The function should return when the game is over.
    The modified board will contain the state of the game,
    so the function does not return anything.
    """
    if board.check_win() != None:
        return
    empty_squares = board.get_empty_squares()
    squares = empty_squares[random.randrange(len(empty_squares))]
    board.move(squares[0], squares[1], player)
    # recursively play the game
    mc_trial(board, provided.switch_player(player))

def get_best_move(board, scores):
    '''
    function find all of the empty squares with the maximum score and
    randomly return one of them as a (row, column) tuple;
    board that has no empty squares results in error message
    '''
    empty_squares = board.get_empty_squares()
    if len(empty_squares) == 0:
        return
    best_move = None
    best_score = None
    for square in empty_squares:
        if best_move == None or scores[square[0]][square[1]] > best_score:
            best_move = square
            best_score = scores[square[0]][square[1]]
    return best_move

def mc_update_scores(scores, board, player):
    '''
    a grid of scores (a list of lists), score the completed board and update the scores grid,
    the function updates the scores grid directly, it does not return anything
    '''
    winner = board.check_win()

    dims = board.get_dim()
    # looping through the grid and assigning scores for win/lose
    for row in range(dims):
        for col in range(dims):
            player = board.square(row, col)
            if player == PLAYERX:
                if winner == PLAYERX:
                    scores[row][col] += SCORE_CURRENT
                elif winner == PLAYERO:
                    scores[row][col] += -SCORE_OTHER
            elif player == PLAYERO:
                if winner == PLAYERX:
                    scores[row][col] += -SCORE_OTHER
                elif winner == PLAYERO:
                    scores[row][col] += SCORE_CURRENT
    
def mc_move(board, player, trials):
    '''
    This function takes a current board, which player the machine player is,
    and the number of trials to run. The function should return a move for the machine player
    in the form of a (row, column) tuple.
    '''
    # creates initial score board with every values sets to 0
    initial_board = [[0 for dummy_col in range(board.get_dim())] for
                      dummy_row in range(board.get_dim())]

    for dummy_trial in range(trials):
        cloned = board.clone()
        mc_trial(cloned, player)
        mc_update_scores(initial_board, cloned, player)
        
    return get_best_move(board, initial_board)
    
    
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
