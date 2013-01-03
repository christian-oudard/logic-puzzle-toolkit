from copy import copy

from constants import (
    BLACK,
    WHITE,
    UNKNOWN,
    CONTRADICTION,
    GIVENS,
    DEBUG,
)
from utility import mdist


class Board(object):
    """
    Implements solving and assumption tracking logic.

    Every non-abstract subclass of board must implement an is_valid function.
    This function returns False if the current state is certainly invalid, or
    True if it is valid or potentially valid.
    """
    def __init__(self):
        self.last_conclusion = None # used for search heuristics
        self.limit = None

    def solve(self, max_depth=1, verify_unique=False):
        if not self.is_valid():
            return False
        Board.early_solution = None
        Board.verify_unique = verify_unique
        Board.max_depth = max_depth
        Board.depth_reached = 0
        Board.is_valid_count = 0
        solve_thread = self.solve_thread(depth=0)
        result = None
        for result in solve_thread:
            if self.limit and Board.is_valid_count > self.limit:
                return
            if result is True:
                self.data = Board.early_solution.data
                return True
            if DEBUG(1):
                if is_success(result):
                    print self
                    print
                elif result == False:
                    print 'board unsolvable'
        if result is False or len(self.unknown_positions) > 0:
            return False # incomplete
        else:
            return True # fully solved

    def solve_thread(self, depth):
        if depth > Board.max_depth:
            return
        if depth > Board.depth_reached:
            Board.depth_reached = depth
        yield None
        while True:
            for result in self.conclusion_thread(depth):
                if result is None:
                    yield None
                elif result is True:
                    yield True
                    return
                else:
                    position, color = result
                    self.last_conclusion = position
                    self.set_value(position, color)
                    Board.is_valid_count += 1
                    if not self.is_valid(position, color):
                        yield False
                        return
                    yield result
                    if not Board.verify_unique and len(self.unknown_positions) == 0:
                        Board.early_solution = self
                        yield True
                        return
                    break # restart while loop, continue searching
            else:
                return # conclusion thread found nothing, stop searching

    def conclusion_thread(self, depth):
        assumption_threads = []
        for pos in self.prioritized_positions():
            for color in (BLACK, WHITE):
                assumption_threads.append(self.assumption_thread(pos, color, depth))
        while assumption_threads:
            finished_threads = []
            for at in assumption_threads:
                result = None
                try:
                    result = at.next()
                except StopIteration:
                    finished_threads.append(at)
                if result is None:
                    pass
                elif result is True:
                    yield True
                    return
                else:
                    yield result
                    return
            for ft in finished_threads:
                assumption_threads.remove(ft)
            yield None # now that all threads have gone once, pass control

    def assumption_thread(self, position, color, depth):
        self.set_value(position, color)
        Board.is_valid_count += 1
        valid = self.is_valid(position, color)
        self.set_value(position, UNKNOWN)
        if not valid:
            yield (position, opposite_color(color))
        yield None
        assumption_board = self.copy()
        assumption_board.set_value(position, color)
        assumption_board.last_conclusion = position
        for result in assumption_board.solve_thread(depth + 1):
            if result is None:
                yield None
            elif result is False:
                yield (position, opposite_color(color))
            elif result is True:
                yield True
                return

    def is_valid(self, position=None, color=None):
        """
        Determine whether a board has a legal or illegal position.

        Each subclass must provide a validity_checks list.
        """
        for valid_func in self.validity_checks:
            if not valid_func(self, position, color):
                return False
        return True

    # optimization #

    def prioritized_positions(self):
        priority_dict = {}
        for pos in self.unknown_positions:
            priority_dict[pos] = self.priority(pos)
        position_list = list(self.unknown_positions)
        return sorted(position_list, key=priority_dict.__getitem__, reverse=True)

    def priority(self, position):
        score = 0
        if self.last_conclusion is not None:
            dist = mdist(position, self.last_conclusion)
            score += max(5 - dist, 0)
        for adj in self.adjacencies[position]:
            if not self.is_unknown(adj):
                score += 1
        return score

    def update_color_caches(self, pos, value):
        if pos in self.black_positions:
            self.black_positions.remove(pos)
        if pos in self.white_positions:
            self.white_positions.remove(pos)
        if pos in self.unknown_positions:
            self.unknown_positions.remove(pos)

        if value == BLACK:
            self.black_positions.add(pos)
        elif value == WHITE or value in GIVENS:
            self.white_positions.add(pos)
        elif value == UNKNOWN:
            self.unknown_positions.add(pos)

    # grid overrides #
    def _in_bounds(self, x, y):
        """Determine whether a particular point is within the hexagonal boundary of the board."""
        return False

    def _adjacencies(self, pos):
        """Return all in-bounds adjacencies of the given position."""
        return []

    def __str__(self):
        return repr(self)

    def copy(self):
        #TODO: implement more precise copying, less shotgun approach.
        new_board = copy(self)
        new_board.data = copy(self.data)
        new_board.positions = copy(self.positions)
        new_board.black_positions = copy(self.black_positions)
        new_board.white_positions = copy(self.white_positions)
        new_board.unknown_positions = copy(self.unknown_positions)
        return new_board

    def is_black(self, pos):
        return self[pos] == BLACK

    def is_white(self, pos):
        value = self[pos]
        return value == WHITE or value in GIVENS # givens are white

    def is_unknown(self, pos):
        return self[pos] == UNKNOWN

    def set_black(self, pos):
        self.set_value(pos, BLACK)

    def set_white(self, pos):
        self.set_value(pos, WHITE)

    def set_unknown(self, pos):
        self.set_value(pos, UNKNOWN)

    def set_value(self, pos, value):
        if pos in self.positions:
            if self[pos] != value:
                self[pos] = value
                self.update_color_caches(pos, value)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __eq__(self, other):
        return self.data == other.data

    def __ne__(self, other):
        return not (self == other)


def opposite_color(color):
    if color == WHITE:
        return BLACK
    if color == BLACK:
        return WHITE
