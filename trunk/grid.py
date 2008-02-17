from board import *

class Grid(Board):
    def __init__(self, data_string):
        super(Grid, self).__init__()
        
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

        # calculate adjacency graphs
        self.adjacencies = {}
        self.corner_adjacencies = {}
        for pos in self.positions:
            self.adjacencies[pos] = self._adjacencies(pos)
            self.corner_adjacencies[pos] = self._corner_adjacencies(pos)

    def _cull_bounds(self, position_list):
        """Remove all positions that are out of bounds, and return the remainder."""
        return [(x,y) for (x,y) in position_list if (x,y) in self.positions]

    def __repr__(self):
        char_grid = [[' '] * (self.max_x + 1) for i in range(self.max_y + 1)]
        for key, value in self.data.iteritems():
            x, y = key
            char_grid[y][x] = chars[value]
        return '\n'.join(''.join(line) for line in char_grid)
