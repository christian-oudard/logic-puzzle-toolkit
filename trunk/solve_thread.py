from copy import copy
from itertools import izip
from constants import *

# a solve thread yields UNKNOWN if nothing was determined,
# a result if a space was solved,
# True for a fully solved board,
# False for giving up,
# and CONTRADICTION if a contradiction was found
class SolveThread(object):
    def __init__(self, board, depth):
        self.board = copy_board(board)
        self.depth = depth
        self.gen = self.generator()

    def __iter__(self):
        return self

    def next(self):
        return self.gen.next()

    def generator(self):
        if DEBUG1(): print 'depth', self.depth
        if DEBUG2(): print self.board
        currently_valid = self.board.is_valid()
        if not currently_valid:
            if DEBUG1(): print 'board unsolvable at depth',self.depth
            yield CONTRADICTION
            raise StopIteration
        else: # board valid
            if self.board.unknown_positions == 0:
                if DEBUG1(): print 'board solved at depth',self.depth
                yield True # board solved
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
            if DEBUG2():
                print 'contradiction'
                print 'invalid board:'
                print self.board
            yield CONTRADICTION
        elif not valid_black:
            yield (self.position, WHITE)
        elif not valid_white:
            yield (self.position, BLACK)
        else:
            yield UNKNOWN

        if self.depth >= self.board.max_depth:
            raise StopIteration
        
        self.board.set_black(self.position)
        if DEBUG2(): print 'assuming', self.position, 'BLACK'
        solve_black = SolveThread(self.board, self.depth + 1)

        self.board.set_white(self.position)
        if DEBUG2(): print 'assuming', self.position, 'WHITE'
        solve_white = SolveThread(self.board, self.depth + 1)
        
## OLD
        contradiction_black = any(result == CONTRADICTION for result in solve_black)
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
##

#        for (result_black, result_white) in izip(solve_black, solve_white):

## BROKEN
#        black_done = False
#        white_done = False
#        c = 0 #DEBUG
#        while not (black_done and white_done):
#            c += 1
#            if DEBUG2(): print 'pass number',c,hash(self)
#            
#            try:
#                result_black = solve_black.next()
#                if result_black == CONTRADICTION:
#                    #yield (self.position, WHITE)
#                    yield (self.position, BLACK)
#                else:
#                    yield UNKNOWN
#            except StopIteration:
#                black_done = True
#            try:
#                result_white = solve_white.next()
#                if result_white == CONTRADICTION:
#                    #yield (self.position, BLACK)
#                    yield (self.position, WHITE)
#                else:
#                    yield UNKNOWN
#            except StopIteration:
#                white_done = True

def copy_board(board):
    new_board = copy(board)
    new_board.data = copy(board.data)
    new_board.positions = copy(board.positions)
    new_board.black_positions = copy(board.black_positions)
    new_board.white_positions = copy(board.white_positions)
    new_board.unknown_positions = copy(board.unknown_positions)
    return new_board
