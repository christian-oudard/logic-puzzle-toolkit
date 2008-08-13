from constants import *
from utility import *

# every non-abstract subclass of board must implement an is_valid function.
# this function returns false if the current state is certainly invalid, or
# true if it is valid or potentially valid

class Board(object):    
    def __init__(self):
        self.last_conclusion = None # used for search heuristics
        self.limit = None
        
    def solve(self, max_depth=2):
        if not self.is_valid():
            return False
        Board.max_depth = max_depth
        Board.depth_reached = 0
        Board.is_valid_count = 0
        solve_thread = self.solve_thread(depth=0)
        result = None
        for result in solve_thread:
            pass
            if self.limit and Board.is_valid_count > self.limit:
                return
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
                else:
                    position, color = result
                    self.last_conclusion = position
                    self.set_value(position, color)
                    Board.is_valid_count += 1
                    if not self.is_valid(position, color):
                        yield False
                        return
                    yield result
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
        assumption_board = copy_board(self)
        assumption_board.set_value(position, color)
        for result in assumption_board.solve_thread(depth + 1):
            if result is None:
                yield None
            elif result is False:
                yield (position, opposite_color(color))


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
            if self.is_black(adj) or self.is_white(adj): # priority up for being next to a known space
                score += 1
            if self[adj] in GIVENS: # priority up for being next to a given
                score += 1
        return score

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
            if self[pos] in GIVENS:
                self.given_positions.add(pos)

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

    # general functions #
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
    def __iter__(self):
        """Iterate through board values."""
        for (x,y) in self.positions:
            yield self.data[y][x]
        

