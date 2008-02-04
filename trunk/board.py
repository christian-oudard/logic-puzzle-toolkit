from copy import deepcopy

# constants
_black = 3
_white = 4
_unknown = 5
_contradiction = -1
_givens = (0,1,2)

solve_debug_display = False

# dictionaries to convert from constants to strings
chars = {
    _black: 'X',
    _white: '.',
    _unknown: ' ',
    _contradiction: '!',
    0: '0',
    1: '1',
    2: '2',
    }
rchars = {}
for item in chars:
    rchars[chars[item]] = item

position_precalc = {} # for each size, contains a list of all positions
adjacency_precalc = {} # for each size, contains a dictionary of the adjacency graph
tower_adjacency_precalc = {} # dictionaries of tower-adjacency graph


class Board(object):
    def __init__(self, initial):
        lines = False
        if type(initial) == str: # if it was actually a string argument
            lines = initial.split('\n')
            try:
                while True:
                    lines.remove('')
            except ValueError: pass
            size = len(lines)
            assert size % 2 == 0 # must be even number of lines
            size /= 2
        else:
            size = int(initial) # just a size for a blank board

        self.size = size
        self.xsize = 6*size - 1
        self.ysize = 2*size

        # allocate array large enough to fit hexagon of side length 'size'
        self.data = []
        for i in range(self.ysize):
            self.data.append([_unknown]*(self.xsize))

        # fill data from string
        if lines:
            y = 0
            for line in lines:
                x = 0
                for c in line:
                    try:
                        n = rchars[c]
                    except IndexError:
                        raise ValueError('Invalid board entry: %r' % c)
                    try:
                        self[(x,y)] = n
                    except IndexError:
                        pass
                    x += 1
                y += 1
        
        # precalculate in-bounds positions
        try:
            self.positions = position_precalc[self.size]
        except KeyError:
            self.positions = []
            for y in range(self.ysize):
                for x in range(self.xsize):
                    if self._in_bounds(x,y):
                        pos = (x,y)
                        self.positions.append(pos)
            position_precalc[self.size] = self.positions
            
        # precalculate adjacency graph
        try:
            self.adjacencies = adjacency_precalc[self.size]
        except KeyError:
            self.adjacencies = {}
            for pos in self.positions:
                self.adjacencies[pos] = tuple(self._adjacencies(pos))
            adjacency_precalc[self.size] = self.adjacencies
            
        # precalculate tower-adjacency graph
        try:
            self.tower_adjacencies = tower_adjacency_precalc[self.size]
        except KeyError:
            self.tower_adjacencies = {}
            for pos in self.positions:
                self.tower_adjacencies[pos] = tuple(self._tower_adjacencies(pos))
            tower_adjacency_precalc[self.size] = self.tower_adjacencies
        

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
                    self[pos] = _contradiction
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

    def prioritized_positions(self):
        if solve_debug_display:
            print 'sort'
        priority_dic = {}
        for pos in self.positions:
            score = 0
            for adj in self.adjacencies[pos]:
                if self.is_black(adj): # priority up for being next to a tower
                    score += 1
                if self[adj] in _givens: # priority up for being next to a given
                    score += 1
                if self.is_white(adj): # priority up for being next to a known white space
                    score += 1            
            priority_dic[pos] = score
        return sorted(self.positions,key=priority_dic.__getitem__, reverse=True)

    def is_valid(self):
        """Determine whether a board has a legal or illegal position."""
        return all((
            self.test_tower_adjacency(),
            self.test_given_numbers(),
            self.test_white_triangles(),
            self.test_tower_loops(),
            self.test_towers_connected(),
        ))


    def test_tower_adjacency(self):
        for pos in self.positions:
            if self.is_black(pos): # found a tower
                for adj in self.adjacencies[pos]:
                    if self.is_black(adj): # with another tower next to it
                        return False
        return True


    def test_given_numbers(self):
        for pos in self.positions:
            number = self[pos]
            if number not in _givens:
                continue
            num_black = 0
            num_white = 0
            adjs = self.adjacencies[pos]
            for adj in adjs:
                if self.is_black(adj):
                    num_black += 1
                elif self.is_white(adj):
                    num_white += 1
            if num_black > number or num_white > (len(adjs) - number):
                return False
        return True


    def test_white_triangles(self):
        # white triangles of size 2 are illegal
        for pos in self.positions: # consider every space and see if it is a center
            if self.is_white(pos):
                adjs = self.adjacencies[pos]
                if len(adjs) == 3: # must not be on the edge of the board
                    if all(self.is_white(a) for a in adjs):
                        return False
        return True


    def test_tower_loops(self):
        marks = {}
        for pos in self.positions:
            if self.is_white(pos) or self.is_unknown(pos):
                marks[pos] = 'unvisited' # init marks

        def search_white(pos):
            marks[pos] = 'visited'
            adjs = self.adjacencies[pos]
            results = []
            for adj in adjs:
                if self.is_black(adj):
                    results.append(_black)
                elif marks[adj] == 'unvisited': # edge or unknown, and unvisited
                    results.append(search_white(adj))
            if len(adjs) < 3: # test this node for being an edge last, so whole group is still searched
                return 'edge'
            if any(r == 'edge' for r in results): # found a path to an edge
                return 'edge'
            return _black # no neighbor returned a path to an edge

        for pos in self.positions: # for every unvisited space
            if pos in marks and marks[pos] == 'unvisited':
                if search_white(pos) == _black:
                    return False

        return True


    def test_towers_connected(self):
        # test that all towers are connected
        marks = {}
        for pos in self.positions:
            if self.is_black(pos) or self.is_unknown(pos):
                marks[pos] = 'unvisited' # init marks

        def search_black(pos): # just mark everything in the group 'visited'
            marks[pos] = 'visited'
            adjs = self.tower_adjacencies[pos]
            for adj in adjs:
                if adj in marks and marks[adj] == 'unvisited':
                    search_black(adj)

        group_count = 0
        for pos in self.positions: # for every unvisited tower
            if self.is_black(pos) and marks[pos] == 'unvisited': # don't start a group with an unknown space
                group_count += 1
                if group_count >= 2:
                    return False
                search_black(pos)

        return True


    def _in_bounds(self, x, y):
        """Determine whether a particular point is within the hexagonal boundary of the board."""
        if y < 0 or y >= self.ysize or x < 0 or x >= self.xsize:
            self.bounds_dict[(x,y)] = False
            return False # outside allocation area

        dist = 2*(self.size - 1)
        fromright = self.xsize - x - 1
        frombottom = self.ysize - y - 1

        # lines creating sides of the hex
        topleft = x + y > dist
        topright = fromright + y > dist
        bottomleft = x + frombottom > dist
        bottomright = fromright + frombottom > dist

        result = topleft and topright and bottomleft and bottomright
        return result


    def cull_bounds(self, position_list):
        """Remove all positions that are out of bounds, and return the remainder."""
        #return [(x,y) for (x,y) in position_list if self.in_bounds(x,y)]
        return [(x,y) for (x,y) in position_list if (x,y) in self.positions]


    def _adjacencies(self, pos):
        """Return all in-bounds adjacencies of the given position."""

        x, y = pos

        adjacency_list = [(x-1,y), (x+1,y)] # add left and right spaces

        if (x+y)%2 == 0: # even triangle, pointing down
            adjacency_list.append((x,y-1))
        else: # odd triangle, pointing up
            adjacency_list.append((x,y+1))

        return self.cull_bounds(adjacency_list)


    def _tower_adjacencies(self, pos):
        """Return all in-bounds corner-adjacencies of the given position."""

        x, y = pos

        # add 2-left, 2-right, and diagonal spaces
        adjacency_list = [(x-2,y), (x+2,y), (x-1,y-1),(x+1,y-1),(x-1,y+1),(x+1,y+1)]

        if (x+y)%2 == 0: # even triangle, pointing down
            adjacency_list.extend([(x,y+1),(x-2,y-1),(x+2,y-1)])
        else: # odd triangle, pointing up
            adjacency_list.extend([(x,y-1),(x-2,y+1),(x+2,y+1)])

        return self.cull_bounds(adjacency_list)


    def is_black(self, pos):
        return self[pos] == _black
    
    def is_white(self, pos):
        return self[pos] == _white or self[pos] in _givens # givens are white
    
    def is_unknown(self, pos):
        return self[pos] == _unknown

    
    def set_black(self, pos):
        self[pos] = _black

    def set_white(self, pos):
        self[pos] = _white

    def set_unknown(self, pos):
        self[pos] = _unknown


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

    def __str__(self):
        s = ''
        height = self.size*4 + 1
        n = 0
        row = 0
        slash = '/'
        iter_self = iter(self)

        while True:
            # border line
            margin = self.size*2 - min(n, height-n-1)
            border_length = self.size + min(row, self.size*2 - row)
            s += ' '*margin
            s += '*---'*border_length + '*\n'
            n += 1

            if not n < height:
                break

            row += 1

            # triangle line
            margin = self.size*2 - min(n, height-n-1)
            row_length = 2*(self.size + min(row, 2*self.size - row + 1))

            s += ' '*margin

            if row == self.size + 1: # adjust slashes after midpoint
                slash = '\\'

            i = 0
            while True:
                s += slash
                if slash == '/': slash = '\\'
                else: slash = '/'
                i += 1
                if not i < row_length:
                    break
                s += chars[iter_self.next()]
                
            s += '\n'
            n += 1

        return s[:-1]
