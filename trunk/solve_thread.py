from copy import copy
from constants import *

# a solve thread yields UNKNOWN if nothing was determined,
# a result if a space was solved,
# True for a fully solved board,
# False for giving up,
# and CONTRADICTION if a contradiction was found
class SolveThread(object):
    def __init__(self, board, depth):
        self.board = board
        self.depth = depth
        self.gen = self.generator()

    def __iter__(self):
        return self

    def next(self):
        return self.gen.next()

    def generator(self):
        self.board = copy_board(self.board)
        if DEBUG1(): print 'depth', self.depth
        if DEBUG2(): print self.board
        if not self.board.is_valid():
            yield CONTRADICTION
            raise StopIteration
        while True:
            for result in self.board.conclusion_thread(self.depth):
                if is_success(result):
                    position, color = result
                    self.board._set_value(position, color)
                    if DEBUG2() or DEBUG1() and self.depth == 1: print self.board
                    yield result
                    break # continue solving. break for loop, continue while loop normally
                elif result == CONTRADICTION:
                    yield CONTRADICTION
                    raise StopIteration
                elif result == UNKNOWN:
                    yield UNKNOWN
            else: # conclusion thread ran out, no more to solve
                break
        # see if board was fully solved
        unknown_count = 0
        for pos in self.board.positions:
            if self.board.is_unknown(pos):
                unknown_count += 1
        if unknown_count > 0:
            yield False # incomplete
        else:
            yield True # fully solved


class AssumptionThread(object):
    def __init__(self, board, position, depth):
        assert(board.is_unknown(position))
        self.board = board
        self.position = position
        self.depth = depth
        self.gen = self.generator()

    def __iter__(self):
        return self

    def next(self):
        return self.gen.next()

    def generator(self):
        self.board = copy_board(self.board)

        self.board.set_black(self.position)
        valid_black = self.board.is_valid()
        self.board.set_white(self.position)
        valid_white = self.board.is_valid()
        
        if not valid_white and not valid_black:
            if DEBUG2(): print 'simple contradiction'
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
        if DEBUG2(): print 'assuming', self.position, 'BLACK'
        solve_black = SolveThread(self.board, self.depth + 1)
        contradiction_black = any(result == CONTRADICTION for result in solve_black)

        self.board.set_white(self.position)
        if DEBUG2(): print 'assuming', self.position, 'WHITE'
        solve_white = SolveThread(self.board, self.depth + 1)
        contradiction_white = any(result == CONTRADICTION for result in solve_white)

        if contradiction_white and contradiction_black:
            if DEBUG2(): print 'deep contradiction'
            yield CONTRADICTION
        elif contradiction_black:
            yield (self.position, WHITE)
        elif contradiction_white:
            yield (self.position, BLACK)
        else:
            yield UNKNOWN

def copy_board(board):
    new_board = copy(board)
    new_board.data = copy(board.data)
    return new_board

