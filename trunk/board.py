from copy import deepcopy

# constants
BLACK = -1
WHITE = -2
UNKNOWN = -3
CONTRADICTION = -4
GIVENS = range(10)

solve_debug_display = False

# dictionaries to convert from constants to strings
chars = {
    BLACK: 'X',
    WHITE: '.',
    UNKNOWN: ' ',
    CONTRADICTION: '!',
    }
for g in GIVENS:
    chars[g] = str(g)
rchars = {}
for item in chars:
    rchars[chars[item]] = item

class Board(object):
    def solve(self, depth=2):
        """Solve the board using recursive search.
        
        If nothing was solved, return 0. If something was solved in n
        steps, return n. If a contradiction was found, return -n.
        """
        
        if depth == 0: # base case, just report if board is valid
            if not self.is_valid():
                return -1 # 1-step contradiction
            else:
                return 0
        
        step_count = 0
        while True:
            for d in range(1,depth+1): # starting with depth 1, increase depth until a conclusion is made
                result = self.make_conclusion(d)
                if result < 0:
                    step_count += abs(result)
                    return -step_count
                elif result > 0: # solved a space, start over from depth 1
                    step_count += result
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

        step_count = 1

        for pos in self.prioritized_positions():
            if self.is_unknown(pos):
                # assume black
                test_board_black = deepcopy(self)
                test_board_black.set_black(pos)
                result_black = test_board_black.solve(depth-1)
                # assume white
                test_board_white = deepcopy(self)
                test_board_white.set_white(pos)
                result_white = test_board_white.solve(depth-1) 
                if (result_white < 0) and (result_black < 0): # contradiction reached, board unsolvable
                    self[pos] = CONTRADICTION
                    return result_white + result_black
                elif (result_black < 0):
                    self.set_white(pos)
                    return abs(result_black)
                elif (result_white < 0):
                    self.set_black(pos)
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
        return self.positions 

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

    def __len__(self):
        return 6*self.size**2
    def __getitem__(self, key):
        (x,y) = key
        return self.data[y][x]
    def __setitem__(self, key, value):
        (x,y) = key
        self.data[y][x] = value
    def __eq__(self, other):
        return self.data == other.data
    def __ne__(self, other):
        return not (self == other)
    def __iter__(self):
        """Iterate through board values."""
        for (x,y) in self.positions:
            yield self.data[y][x]
    def __deepcopy__(self, memo={}):
        result = self.__class__(self.size)
        memo[id(self)] = result
        result.data = deepcopy(self.data, memo)
        return result
