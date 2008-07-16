from copy import copy
from constants import *

class SolveThread(object):
    def __init__(self, board, position, depth):
        assert(board.is_unknown(position))
        self.board = board
        self.position = position
        self.depth = depth
        self.gen = self.generator()

    def copy_board(self):
        """
        Make a copy of the board.

        This is done lazily, the first time the generator is advanced, instead of at object creation time.
        """

        self.board = copy(self.board)
        self.board.data = copy(self.board.data)

    def __iter__(self):
        return self

    def next(self):
        return self.gen.next()

    def generator(self):
        self.copy_board()

        self.board.set_black(self.position)
        valid_black = self.board.is_valid()
        self.board.set_white(self.position)
        valid_white = self.board.is_valid()
        
        if not valid_white and not valid_black:
            if DEBUG: print 'simple contradiction'
            yield CONTRADICTION
        elif not valid_black:
            yield (self.position, WHITE)
        elif not valid_white:
            yield (self.position, BLACK)
        else:
            yield UNKNOWN

        # recurse to deeper level
        #TODO make solve call incremental here
        # and reduce code duplication
        if self.depth >= self.board.max_depth:
            raise StopIteration
        
        self.board.set_black(self.position)
        if DEBUG: print 'assuming', self.position, 'BLACK'
        result = self.board._solve(self.depth+1)
        if result == CONTRADICTION:
            contradiction_black = True
        elif result == True:
            pass #STUB board is solved
        elif result == False:
            contradiction_black = False

        self.board.set_white(self.position)
        if DEBUG: print 'assuming', self.position, 'WHITE'
        result = self.board._solve(self.depth+1)
        if result == CONTRADICTION:
            contradiction_white = True
        elif result == True:
            pass #STUB board is solved
        elif result == False:
            contradiction_white = False

        if contradiction_white and contradiction_black:
            if DEBUG: print 'deep contradiction'
            yield CONTRADICTION
        elif contradiction_black:
            yield (self.position, WHITE)
        elif contradiction_white:
            yield (self.position, BLACK)
        else:
            yield UNKNOWN


