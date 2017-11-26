class SolitaireMancala(object):
    '''
    class to run the game logic
    '''
    def __init__(self):
        self.state = [0]
        
    def set_board(self, configuration):
        '''
        board to be a copy of the supplied configuration
        '''
        self.state = configuration[:]
        
    def __str__(self):
        '''
        string corresponding to the current configuration of the board
        '''
        # logic of the game and internal representation are reversed
        return str(self.state[::-1])
        
    def get_num_seeds(self, house_num):
        '''
        return the number of seeds in the house with index house_num
        '''
        return self.state[house_num]        

    def is_legal_move(self, house_num):
        '''
        return True if moving the seeds from house house_num is legal;
        if house_num is zero, is_legal_move should return False
        '''
        # a move is legal if house value equals to its distance from the store
        return self.state[house_num] == house_num and house_num != 0

    def is_game_won(self):
        '''
        return True if all houses contain no seeds
        '''
        # check if all positions (except for the store) are empty
        return sum(self.state[1:]) == 0
    
    def apply_move(self, house_num):
        '''
        apply a legal move for house house_num to the board
        '''
        if self.is_legal_move(house_num):
            # adding +1 to each position lying in front of (and excluding) house_num
            for position in xrange(len(self.state[:house_num])):
                self.state[position] += 1
            # current house (house_num) is then emptied
            self.state[house_num] = 0
        else:
            print 'No can do, this is a illegal move!'
    
    def choose_move(self):
        '''
        return the index for the legal move whose house is closest to the store;
        if no legal move is available, return 0
        '''
        # if no legal move found, need to eventually return 0
        index = 0
        # checking through each position backwards just to arrive at closest one
        for num in range(len(self.state))[::-1]:
            if self.is_legal_move(num):
                index = num
        return index

    def plan_moves(self):
        '''
        return a list of legal moves computed to win the game if possible
        '''
        legal_moves = []
        # game isn't won yet and there is still at least one legal move
        while not self.is_game_won() and self.choose_move() != 0:
            # make a note of and apply every possible move suggested
            legal_moves.append(self.choose_move())
            self.apply_move(self.choose_move())
        return legal_moves
    
import random

########################
class SolitaireMancala2(object):
    def __init__(self):
        self._board = [0]

    def set_board(self, configuration):
        self._board = configuration[:]

    def __str__(self):
        return str([self._board[i] for i in range((len(self._board) - 1), (-1), (-1))])

    def get_num_seeds(self, house_num):
        return self._board[house_num]

    def is_legal_move(self, house_num):
        if ((house_num == 0) or (house_num >= len(self._board))):
            return False
        else:
            return (house_num == self._board[house_num])

    def apply_move(self, house_num):
        if self.is_legal_move(house_num):
            for i in range(house_num):
                self._board[i] += 1
            self._board[house_num] = 0

    def choose_move(self):
        for i in self._board[1:]:
            if self.is_legal_move(i):
                return i
        return 0

    def is_game_won(self):
        won = True
        for i in self._board[1:]:
            if (i != 0):
                won = False
        return won

    def plan_moves1(self):
        moves = []
        count = 0
        temp_store = self._store[:]
        while ((not self.is_game_won()) and (count < 100)):
            move = self.choose_move()
            moves.append(move)
            self.apply_move(move)
            count += 1
        self._store = temp_store[:]
        return moves
    
    #28
    def plan_moves2(self):
        plan = []
        while (not self.is_game_won()):
            if (self.choose_move() > 0):
                plan.append(self.choose_move())
                self.apply_move(self.choose_move())
            else:
                return []
        return plan
    
    #41
    def plan_moves3(self):
        moves = []
        while True:
            move = self.choose_move()
            if ((move == 0) or self.is_game_won()):
                break
            else:
                self.apply_move(move)
                moves.append(move)
        return moves
    
TEST_CASES = []
for i in range(10000):
    config = [0]
    length = random.randint(1,9)
    for j in range(length):
        config.append(random.randint(0,10))
    correct = SolitaireMancala()
    incorrect = SolitaireMancala2()
    correct.set_board(config)
    incorrect.set_board(config)
    correct_list = correct.plan_moves()
    incorrect_list = incorrect.plan_moves3()
    if correct_list != incorrect_list:
        TEST_CASES.append(config)
        
        
#print TEST_CASES
TEST_CASES = [[0, 7, 8], [0, 2, 2, 6, 4, 9, 1, 3, 5, 8], [0, 4, 5, 6, 4], [0, 7, 4, 3, 4], [0, 1, 2, 2, 3, 1, 3, 5, 7, 9], [0, 1, 1, 1, 0, 2, 4, 6, 8], [0, 0, 2], [0, 1, 1, 3], [0], [0, 1, 2, 0, 2, 4, 6]]
