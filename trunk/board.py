from constants import *
from solve_thread import SolveThread, AssumptionThread

class Board(object):    
    def __init__(self):
        self.last_conclusion = None
        self._valid = None
        
    def solve(self, max_depth=2):
        self.max_depth = max_depth
        solve_thread = SolveThread(self, 1)
        for result in solve_thread:
            pass
        self.data = solve_thread.board.data
        return result

    def conclusion_thread(self, depth):
        assumption_threads = []
        for pos in self.prioritized_positions():
            if self.is_unknown(pos):
                assumption_threads.append(AssumptionThread(self, pos, depth))
        while len(assumption_threads) > 0:
            finished_threads = []
            for at in assumption_threads:
                try:
                    result = at.next()
                except StopIteration:
                    # thread finished, delete it
                    finished_threads.append(at)
                    break
                if is_success(result):
                    if DEBUG2(): print 'level', depth, 'found:', result
                    yield result
                    raise StopIteration
                elif result == CONTRADICTION:
                    yield CONTRADICTION
                else:
                    yield UNKNOWN
            for ft in finished_threads:
                assumption_threads.remove(ft)
        # all threads exited with no conclusion, quit
        if DEBUG2(): print 'no threads left, quit'

    # puzzle overrides #
    def is_valid(self):
        """Determine whether a board has a legal or illegal position."""
        if self._valid is not None:
            return self._valid
        else:
            self._valid = self._is_valid()
            return self._valid

    def prioritized_positions(self):
        if DEBUG2(): print 'sort'
        priority_dic = {}
        for pos in self.positions:
            score = 0
            if self.last_conclusion is not None:
                dist = mdist(pos, self.last_conclusion)
                score += max(5 - dist, 0)
            for adj in self.adjacencies[pos]:
                if self.is_black(adj) or self.is_white(adj): # priority up for being next to a known space
                    score += 1
                if self[adj] in GIVENS: # priority up for being next to a given
                    score += 1
            priority_dic[pos] = score
        return sorted(self.positions, key=priority_dic.__getitem__, reverse=True)

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
        return self[pos] == WHITE or self[pos] in GIVENS # givens are white
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
                self._valid = None # clear is_valid cache
                self[pos] = value
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
def mdist(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)

