from itertools import izip
from iterators import izip_longest, imix
from constants import *

# every non-abstract subclass of board must implement an is_valid function.
# this function returns false if the current state is certainly invalid, or
# true if it is valid or potentially valid

# debug levels
# 1: show start and solved state
# 2: show steps in between
# 3: show details of solving

class Board(object):    
    def __init__(self):
        self.last_conclusion = None # used for search heuristics
        
    def solve(self, max_depth=2):
        self.max_depth = max_depth
        Board.depth_reached = 0
        if DEBUG(3): print 'solving to depth', max_depth
        elif DEBUG(1): print 'solving...'
        if DEBUG(1): print self
        if not self.is_valid():
            return CONTRADICTION
        solve_thread = self.solve_thread(depth=1)
        result = None
        for result in solve_thread:
            if DEBUG(2):
                if is_success(result):
                    pos, color = result
                    print pos, '=', CHARS[color]
                    print self
        if DEBUG(1):
            if result == True:
                print 'solved'
            elif result == False:
                print 'unable to solve'
            elif result == CONTRADICTION:
                print 'unsolvable'
            print self
        if DEBUG(2): print 'greatest depth reached:', Board.depth_reached
        return result

    # a solve thread yields UNKNOWN if nothing was determined,
    # a result if a space was solved,
    # True for a fully solved board,
    # False for giving up,
    # and CONTRADICTION if a contradiction was found
    def solve_thread(self, depth):
        if depth > self.max_depth:
            return
        if DEBUG(3): print 'level', depth
        if depth > Board.depth_reached:
            Board.depth_reached = depth
        while True:
            assumption_threads = [self.assumption_thread(pos, depth) for pos in self.prioritized_positions()]
            for result in imix(*assumption_threads):
                if result == UNKNOWN:
                    yield UNKNOWN
                elif is_success(result):
                    position, color = result
                    self.last_conclusion = position
                    self._set_value(position, color)
                    if DEBUG(4):
                        print self
                    yield result
                    break # restart while loop. clear threads, continue searching
                elif result == CONTRADICTION:
                    yield CONTRADICTION
                    return
            else: # no more to solve
                break
        if len(self.unknown_positions) > 0:
            yield False # incomplete
        else:
            yield True # fully solved

    def assumption_thread(self, position, depth):
        black_board = copy_board(self)
        black_board.set_black(position)
        valid_black = black_board.is_valid()

        white_board = copy_board(self)
        white_board.set_white(position)
        valid_white = white_board.is_valid()

        if not valid_white and not valid_black:
            yield CONTRADICTION
        elif not valid_black:
            yield (position, WHITE)
        elif not valid_white:
            yield (position, BLACK)
        else:
            yield UNKNOWN
        
        solve_black = black_board.solve_thread(depth + 1)
        solve_white = white_board.solve_thread(depth + 1)
        
        # look for results in parallel, until one returns
        for (result_black, result_white) in izip_longest(solve_black, solve_white):
            if result_black == True or result_white == True:
                pass #print 'early solution found'
            if result_black == CONTRADICTION:
                yield (position, WHITE)
            elif result_white == CONTRADICTION:
                yield (position, BLACK)
            else:
                yield UNKNOWN

    # optimization #
    def prioritized_positions(self):
        priority_dict = {}
        for pos in self.unknown_positions:
            score = 0
            if self.last_conclusion is not None:
                dist = mdist(pos, self.last_conclusion)
                score += max(5 - dist, 0)
            for adj in self.adjacencies[pos]:
                if self.is_black(adj) or self.is_white(adj): # priority up for being next to a known space
                    score += 1
                if self[adj] in GIVENS: # priority up for being next to a given
                    score += 1
            priority_dict[pos] = score
        position_list = list(self.unknown_positions)
        return sorted(position_list, key=priority_dict.__getitem__, reverse=True)

    def precalc_adjacency(self):
        # calculate adjacency graphs
        self.adjacencies = {}
        self.corner_adjacencies = {}
        for pos in self.positions:
            self.adjacencies[pos] = self._adjacencies(pos)
            self.corner_adjacencies[pos] = self._corner_adjacencies(pos)

    def precalc_positions(self):
        # in-bounds position list
        self.positions = set()
        for key, value in self.data.iteritems():
            if value != OUT_OF_BOUNDS:
                self.positions.add(key)
        # positions by color
        self.black_positions = set()
        self.white_positions = set()
        self.unknown_positions = set()
        self.given_positions = set()
        for pos in self.positions:
            self.update_color_caches(pos, self[pos])

    def update_color_caches(self, pos, value):
        if pos in self.black_positions:
            self.black_positions.remove(pos)
        if pos in self.white_positions:
            self.white_positions.remove(pos)
        if pos in self.unknown_positions:
            self.unknown_positions.remove(pos)
        if pos in self.given_positions:
            self.given_positions.remove(pos)

        if value == BLACK:
            self.black_positions.add(pos)
        elif value == WHITE or value in GIVENS:
            self.white_positions.add(pos)
        elif value == UNKNOWN:
            self.unknown_positions.add(pos)
        if value in GIVENS:
            self.given_positions.add(pos)

    # grid overrides #
    def _in_bounds(self, x, y):
        """Determine whether a particular point is within the hexagonal boundary of the board."""
        return False
    
    def _adjacencies(self, pos):
        """Return all in-bounds adjacencies of the given position."""
        return []

    def __str__(self):
        return repr(self)

    # general functions #
    def is_black(self, pos):
        return self[pos] == BLACK
    def is_white(self, pos):
        value = self[pos]
        return value == WHITE or value in GIVENS # givens are white
    def is_unknown(self, pos):
        return self[pos] == UNKNOWN

    def set_black(self, pos):
        self._set_value(pos, BLACK)  
    def set_white(self, pos):
        self._set_value(pos, WHITE)
    def set_unknown(self, pos):
        self._set_value(pos, UNKNOWN)
    def _set_value(self, pos, value):
        if pos in self.positions:
            if self[pos] != value:
                self[pos] = value
                self.update_color_caches(pos, value)
    set_number = _set_value    

    def __getitem__(self, key):
        return self.data[key]
    def __setitem__(self, key, value):
        self.data[key] = value
    def __eq__(self, other):
        return self.data == other.data
    def __ne__(self, other):
        return not (self == other)
    def __iter__(self):
        """Iterate through board values."""
        for (x,y) in self.positions:
            yield self.data[y][x]
        

# utility functions #
from copy import copy
def copy_board(board):
    new_board = copy(board)
    new_board.data = copy(board.data)
    new_board.positions = copy(board.positions)
    new_board.black_positions = copy(board.black_positions)
    new_board.white_positions = copy(board.white_positions)
    new_board.unknown_positions = copy(board.unknown_positions)
    return new_board

def mdist(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)

