from copy import copy
from constants import *

class SolveThread(object):
    def __init__(self, board, position, color):
        self.board = copy(board)
        self.board.data = copy(board.data)
        self.position = position
        self.color = color
        self.board._set_value(position, color)
        self.gen = self.generator()

    def __iter__(self):
        return self

    def next(self):
        return self.gen.next()

    def generator(self):
        # first call, check depth 0
        if not self.board.is_valid():
            yield self.success()
        else:
            yield UNKNOWN

    def opposite_color(self):
        if self.color == BLACK:
            return WHITE
        elif self.color == WHITE:
            return BLACK

    def success(self):
        # propagate board changes upward
        self.board._set_value(self.position, self.opposite_color())
        return True

