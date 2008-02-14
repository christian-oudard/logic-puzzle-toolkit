from board import *

class TriangleGrid(Board):
    def __init__(self, data_string):
        lines = data_string.split('\n')
        try:
            while True: # remove blank lines
                lines.remove('')
        except ValueError: pass

        # fill data from string
        init_data = {}
        y = 0
        for line in lines:
            x = 0
            for c in line:
                try:
                    n = rchars[c]
                    init_data[(x,y)] = n
                except KeyError:
                    pass # invalid characters are not included
                x += 1
            y += 1
    
        # bounds correction
        x_vals = []
        y_vals = []
        for pos in init_data.keys():
            x, y = pos
            x_vals.append(x)
            y_vals.append(y)
        min_x, max_x = min(x_vals), max(x_vals)
        min_y, max_y = min(y_vals), max(y_vals)
        self.data = {}
        for key, value in init_data.iteritems():
            x, y = key
            self.data[(x-min_x, y-min_y)] = value
        self.max_x = max_x - min_x
        self.max_y = max_y - min_y

        # in-bounds position list
        self.positions = []
        for key, value in self.data.iteritems():
            if value != OUT_OF_BOUNDS:
                self.positions.append(key)
        
        # precalculate adjacency graphs
        self.adjacencies = {}
        self.corner_adjacencies = {}
        for pos in self.positions:
            self.adjacencies[pos] = self._adjacencies(pos)
            self.corner_adjacencies[pos] = self._corner_adjacencies(pos)
        
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

    def __str__(self):
        char_grid = [[' '] * (self.max_x + 1) for i in range(self.max_y + 1)]
        for key, value in self.data.iteritems():
            x, y = key
            char_grid[y][x] = chars[value]
        return '\n'.join(''.join(line) for line in char_grid)
        
        #while True:
            ## border line
            #margin = self.size*2 - min(n, height-n-1)
            #border_length = self.size + min(row, self.size*2 - row)
            #s += ' '*margin
            #s += '*---'*border_length + '*\n'
            #n += 1

            #if not n < height:
                #break

            #row += 1

            ## triangle line
            #margin = self.size*2 - min(n, height-n-1)
            #row_length = 2*(self.size + min(row, 2*self.size - row + 1))

            #s += ' '*margin

            #if row == self.size + 1: # adjust slashes after midpoint
                #slash = '\\'

            #i = 0
            #while True:
                #s += slash
                #if slash == '/': slash = '\\'
                #else: slash = '/'
                #i += 1
                #if not i < row_length:
                    #break
                #s += chars[iter_self.next()]
                
            #s += '\n'
            #n += 1

        #return s[:-1]


import unittest

class TestTriangleGrid(unittest.TestCase):
    def test_adjacencies(self):
        b = TriangleGrid('''
        ---
        ---''')
        for pos in b.positions:
            for adj in b.adjacencies[pos]:
                self.assert_(pos in b.adjacencies[adj])
                
    def test_corner_adjacencies(self):
        b = TriangleGrid('''
        ---
        ---''')
        for pos in b.positions:
            for adj in b.corner_adjacencies[pos]:
                self.assert_(pos in b.corner_adjacencies[adj])

if __name__ == '__main__':
    unittest.main()
    