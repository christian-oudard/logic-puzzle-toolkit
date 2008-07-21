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
        currently_valid = self.board.is_valid()
        if not currently_valid:
            yield CONTRADICTION
            raise StopIteration
        else: # board valid
            if self.board.unknown_positions == 0:
                yield True # board solved
                raise StopIteration
        if self.depth > self.board.max_depth:
            raise StopIteration
        while True:
            for result in self.board.conclusion_thread(self.depth):
                if is_success(result):
                    position, color = result
                    self.board._set_value(position, color)
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
        solve_black = SolveThread(self.board, self.depth + 1)

        self.board.set_white(self.position)
        solve_white = SolveThread(self.board, self.depth + 1)
        
        contradiction_black = any(result == CONTRADICTION for result in solve_black)
        contradiction_white = any(result == CONTRADICTION for result in solve_white)

        if contradiction_white and contradiction_black:
            yield CONTRADICTION
        elif contradiction_black:
            yield (self.position, WHITE)
        elif contradiction_white:
            yield (self.position, BLACK)
        else:
            yield UNKNOWN

## WRONG
#        for (result_black, result_white) in izip(solve_black, solve_white):
#            if result_black == CONTRADICTION:
#                yield (self.position, WHITE)
#                break
#            elif result_white == CONTRADICTION:
#                yield (self.position, BLACK)
#                break
#
## BROKEN
#        black_done = False
#        white_done = False
#        while not (black_done and white_done):
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

