from copy import copy
from constants import *
from solve_thread import SolveThread

class Board(object):    
    def __init__(self):
        self.last_conclusion = None
        self._valid = None
        
    def solve(self, max_depth=2):
        self.max_depth = max_depth
        return self._solve(1)

    def _solve(self, depth):
        """ Solve the board using a breadth-first search."""
        if DEBUG: print self
        if not self.is_valid():
            return CONTRADICTION
        while True:
            for result in self.conclusion_thread(depth):
                if is_success(result):
                    position, color = result
                    self._set_value(position, color)
                    if DEBUG: print self
                    break # continue while loop
                elif result == CONTRADICTION:
                    return CONTRADICTION
            else: # conclusion thread ran out, no more to solve
                break
        # see if board was fully solved
        unknown_count = 0
        for pos in self.positions:
            if self.is_unknown(pos):
                unknown_count += 1
        if unknown_count > 0:
            return False # not fully solved yet
        else:
            return True # fully solved

    def conclusion_thread(self, depth):
        solve_threads = []
        for pos in self.positions:
            if self.is_unknown(pos):
                solve_threads.append(SolveThread(self, pos, depth))
        while len(solve_threads) > 0:
            if DEBUG: print '.'
            finished_threads = []
            for st in solve_threads:
                try:
                    result = st.next()
                except StopIteration:
                    # thread finished, delete it
                    finished_threads.append(st)
                    break
                if is_success(result):
                    if DEBUG: print 'level', depth, 'found:', result
                    yield result
                    raise StopIteration
                elif result == CONTRADICTION:
                    yield CONTRADICTION
                else:
                    yield UNKNOWN
            for ft in finished_threads:
                if DEBUG: print 'o'
                solve_threads.remove(ft)
        # all threads exited with no conclusion, quit
        if DEBUG: print 'no threads left, quit'

    def old_solve(self, depth=2):
        """Solve the board using recursive search.
        
        Solve until there is nothing left to solve, then return False.
        If a contradiction is reached, return CONTRADICTION.
        """
        
        global abort
        if abort:
            return False
        self.data = copy(self.data)
        
        if depth == 0: # base case, just report if board is valid
            if not self.is_valid():
                return CONTRADICTION # 1-step contradiction
            else:
                return False
        
        while True:
            for d in range(1,depth+1): # starting with depth 1, increase depth until a conclusion is made
                result = self.make_conclusion(d)
                if result == CONTRADICTION:
                    return CONTRADICTION
                elif result == True: # solved a space, start over from depth 1
                    if solve_report and depth == 2:
                        print self
                        print                        
                    if solve_debug_display:
                        if depth >= 2:
                            print 'conclusion'
                        else:
                            print 'try'
                        print self
                    break
                elif result == False: # no more spaces to solve at this depth
                    if solve_debug_display:
                        print 'deadend'
                    #TODO, test if whole board has been solved
                    continue
            else: # max depth reached, done solving
                return False


    def make_conclusion(self, depth):
        """Make one conclusion about board with specified depth.
        
        If nothing was solved, return False. If something was solved,
        return True. If a contradiction was found, return CONTRADICTION.
        """

        global abort
        if abort:
            return False
        global max_steps

        for pos in self.prioritized_positions():
            if max_steps is not None:
                max_steps -= 1
                if max_steps <= 0:
                    abort = True
                    return False
            if self.is_unknown(pos):
                # assume black
                test_board_black = copy(self)
                test_board_black.set_black(pos)
                result_black = test_board_black.solve(depth-1)
                # assume white
                test_board_white = copy(self)
                test_board_white.set_white(pos)
                result_white = test_board_white.solve(depth-1) 
                if result_white == CONTRADICTION and result_black == CONTRADICTION: # contradiction reached, board unsolvable
                    self[pos] = CONTRADICTION
                    return CONTRADICTION
                elif result_black == CONTRADICTION:
                    self.set_white(pos)
                    self.last_conclusion = pos
                    return True
                elif result_white == CONTRADICTION:
                    self.set_black(pos)
                    self.last_conclusion = pos
                    return True
                else: # no contradictions either way
                    self.set_unknown(pos)
                    if solve_debug_display:
                        print '.',
        return False # no spaces determinable


    # puzzle overrides #
    def is_valid(self):
        """Determine whether a board has a legal or illegal position."""
        if self._valid is not None:
            return self._valid
        else:
            self._valid = self._is_valid()
            return self._valid

    def prioritized_positions(self):
        if solve_debug_display:
            print 'sort'
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

