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
        if not valid_black:
            yield (self.position, WHITE)
        else:
            yield UNKNOWN

        self.board.set_white(self.position)
        valid_white = self.board.is_valid()
        if not valid_white and not valid_black:
            yield CONTRADICTION
        elif not valid_white:
            yield (self.position, BLACK)
        else:
            yield UNKNOWN

        #STUB, recurse to deeper level
        #depth-1

