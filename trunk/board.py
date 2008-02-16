from copy import copy

# constants
BLACK = -1
WHITE = -2
UNKNOWN = -3
OUT_OF_BOUNDS = -4
CONTRADICTION = -5
GIVENS = range(36)

max_steps = None
abort = False
solve_debug_display = False
solve_report = False

# dictionaries to convert from constants to strings
chars = {
    BLACK: 'X',
    WHITE: '.',
    UNKNOWN: '-',
    OUT_OF_BOUNDS: '*',
    CONTRADICTION: '!',
    }
for g in range(10):
    chars[g] = str(g) # digits 0 through 9
for g in range(26):
    chars[g + 10] = chr(ord('A') + g) # A = 10 through Z = 35
rchars = {}
for item in chars:
    rchars[chars[item]] = item

class Board(object):    
    def __init__(self):
        self.last_conclusion = None
        
    def solve(self, depth=2):
        """Solve the board using recursive search.
        
        If nothing was solved, return 0. If something was solved in n
        steps, return n. If a contradiction was found, return -n.
        """
        
        global abort
        if abort:
            return
        self.data = copy(self.data)
        
        if depth == 0: # base case, just report if board is valid
            if not self.is_valid():
                return -1 # 1-step contradiction
            else:
                return 0
        
        step_count = 0
        while True:
            for d in range(1,depth+1): # starting with depth 1, increase depth until a conclusion is made
                result = self.make_conclusion(d)
                if result is None:
                    return
                if result < 0:
                    step_count += abs(result)
                    return -step_count
                elif result > 0: # solved a space, start over from depth 1
                    step_count += result
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
                elif result == 0:
                    if solve_debug_display:
                        print 'deadend'
                    #TODO, test if whole board has been solved
                    continue # no more spaces to solve at this depth
            else: # max depth reached, done solving
                return step_count


    def make_conclusion(self, depth):
        """Make one conclusion about board with specified depth.
        
        If nothing was solved, return 0. If something was solved in n
        steps, return n. If a contradiction was found, return -n.
        """

        global abort
        if abort:
            return
        global max_steps
        step_count = 1

        for pos in self.prioritized_positions():
            if max_steps is not None:
                max_steps -= 1
                if max_steps <= 0:
                    global abort
                    abort = True
                    return
            if self.is_unknown(pos):
                # assume black
                test_board_black = copy(self)
                test_board_black.set_black(pos)
                result_black = test_board_black.solve(depth-1)
                # assume white
                test_board_white = copy(self)
                test_board_white.set_white(pos)
                result_white = test_board_white.solve(depth-1) 
                if (result_white < 0) and (result_black < 0): # contradiction reached, board unsolvable
                    self[pos] = CONTRADICTION
                    return result_white + result_black
                elif (result_black < 0):
                    self.set_white(pos)
                    self.last_conclusion = pos
                    return abs(result_black)
                elif (result_white < 0):
                    self.set_black(pos)
                    self.last_conclusion = pos
                    return abs(result_white)
                else: # no contradictions either way
                    self.set_unknown(pos)
                    if solve_debug_display:
                        print '.',
        return 0 # no spaces determinable


    # puzzle overrides #
    def is_valid(self):
        """Determine whether a board has a legal or illegal position."""
        return True

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
        return sorted(self.positions,key=priority_dic.__getitem__, reverse=True)

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
        self[pos] = BLACK
    def set_white(self, pos):
        self[pos] = WHITE
    def set_unknown(self, pos):
        self[pos] = UNKNOWN

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
