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
        self.board = board
        self.depth = depth
        self.gen = self.generator()

    def __iter__(self):
        return self

    def next(self):
        return self.gen.next()

    def generator(self):
        valid = self.board.is_valid()
        if not valid:
            yield CONTRADICTION
            return
        else: # board valid
            if self.board.unknown_positions == 0:
                yield True # board solved
                return
        if self.depth > self.board.max_depth:
            return
        while True:
            for result in self.board.conclusion_thread(self.depth):
                if is_success(result):
                    position, color = result
                    self.board._set_value(position, color)
                    yield result
                    break # continue solving. break for loop, continue while loop normally
                elif result == CONTRADICTION:
                    yield CONTRADICTION
                    return
                elif result == UNKNOWN:
                    yield UNKNOWN
            else: # conclusion thread ran out, no more to solve
                break
        if len(self.board.unknown_positions) > 0:
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
        black_board = copy_board(self.board)
        black_board.set_black(self.position)
        valid_black = black_board.is_valid()

        white_board = copy_board(self.board)
        white_board.set_white(self.position)
        valid_white = white_board.is_valid()
        
        solve_black = SolveThread(black_board, self.depth + 1)
        solve_white = SolveThread(white_board, self.depth + 1)
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
            
def copy_board(board):
    new_board = copy(board)
    new_board.data = copy(board.data)
    new_board.positions = copy(board.positions)
    new_board.black_positions = copy(board.black_positions)
    new_board.white_positions = copy(board.white_positions)
    new_board.unknown_positions = copy(board.unknown_positions)
    return new_board

