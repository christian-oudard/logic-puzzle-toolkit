from board import *

class TriangleGrid(Board):
    position_precalc = {} # for each size, contains a list of all positions
    adjacency_precalc = {} # for each size, contains a dictionary of the adjacency graph
    corner_adjacency_precalc = {} # dictionaries of tower-adjacency graph

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
            self.data.append([UNKNOWN]*(self.xsize))

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
            self.positions = TriangleGrid.position_precalc[self.size]
        except KeyError:
            self.positions = []
            for y in range(self.ysize):
                for x in range(self.xsize):
                    if self._in_bounds(x,y):
                        pos = (x,y)
                        self.positions.append(pos)
            TriangleGrid.position_precalc[self.size] = self.positions
            
        # precalculate adjacency graph
        try:
            self.adjacencies = TriangleGrid.adjacency_precalc[self.size]
        except KeyError:
            self.adjacencies = {}
            for pos in self.positions:
                self.adjacencies[pos] = tuple(self._adjacencies(pos))
            TriangleGrid.adjacency_precalc[self.size] = self.adjacencies
            
        # precalculate tower-adjacency graph
        try:
            self.corner_adjacencies = TriangleGrid.corner_adjacency_precalc[self.size]
        except KeyError:
            self.corner_adjacencies = {}
            for pos in self.positions:
                self.corner_adjacencies[pos] = tuple(self._corner_adjacencies(pos))
            TriangleGrid.corner_adjacency_precalc[self.size] = self.corner_adjacencies
        

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


    def _cull_bounds(self, position_list):
        """Remove all positions that are out of bounds, and return the remainder."""
        return [(x,y) for (x,y) in position_list if (x,y) in self.positions]


    def _adjacencies(self, pos):
        """Return all in-bounds adjacencies of the given position."""

        x, y = pos

        adjacency_list = [(x-1,y), (x+1,y)] # add left and right spaces

        if (x+y)%2 == 0: # even triangle, pointing down
            adjacency_list.append((x,y-1))
        else: # odd triangle, pointing up
            adjacency_list.append((x,y+1))

        return self._cull_bounds(adjacency_list)


    def _corner_adjacencies(self, pos):
        """Return all in-bounds corner-adjacencies of the given position."""

        x, y = pos

        # add 2-left, 2-right, and diagonal spaces
        adjacency_list = [(x-2,y), (x+2,y), (x-1,y-1),(x+1,y-1),(x-1,y+1),(x+1,y+1)]

        if (x+y)%2 == 0: # even triangle, pointing down
            adjacency_list.extend([(x,y+1),(x-2,y-1),(x+2,y-1)])
        else: # odd triangle, pointing up
            adjacency_list.extend([(x,y-1),(x-2,y+1),(x+2,y+1)])

        return self._cull_bounds(adjacency_list)

    def __repr__(self):
        s = ''
        for line in self.data:
            for c in line:
                s += chars[c]
            s += '\n'
        return s
                
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


import unittest

class TestTriangleGrid(unittest.TestCase):
    def test_adjacencies(self):
        b = TriangleGrid(3)
        for pos in b.positions:
            for adj in b.adjacencies[pos]:
                self.assert_(pos in b.adjacencies[adj])
                
    def test_corner_adjacencies(self):
        b = TriangleGrid(3)
        for pos in b.positions:
            for adj in b.corner_adjacencies[pos]:
                self.assert_(pos in b.corner_adjacencies[adj])

if __name__ == '__main__':
    unittest.main()