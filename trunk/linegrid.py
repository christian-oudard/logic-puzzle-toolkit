from constants import *
from grid import Grid

class LineGrid(Grid):
    def __init__(self, data_string):
        Grid.__init__(self, data_string)
        self.precalc_given_adjacencies()
        self.precalc_junctions()
        self.precalc_junction_adjacencies()

    def precalc_given_adjacencies(self):
        self.given_adjacencies = {}
        for pos in self.givens.keys():
            self.given_adjacencies[pos] = self._given_adjacencies(pos)

    def _adjacencies(self, pos):
        x, y = pos
        adjacencies = [
            (x-1, y-1),
            (x-1, y+1),
            (x+1, y-1),
            (x+1, y+1),
        ]
        if LineGrid.is_vertical(pos):
            adjacencies.extend([
                (x, y-2),
                (x, y+2),
            ])
        else: # horizontal
            adjacencies.extend([
                (x-2, y),
                (x+2, y),
            ])
        return self.cull_bounds(adjacencies)

    def _given_adjacencies(self, given_pos):
        x, y = given_pos
        x = x * 2 + 1
        y = y * 2 + 1
        return self.cull_bounds([(x-1, y),
                                  (x+1, y),
                                  (x, y-1),
                                  (x, y+1)])

    NODE_CHAR = '+'
    VERTICAL_CHAR = '|'
    HORIZONTAL_CHAR = '-'
    UNKNOWN_CHAR = ' '

    def translate_data(self, data_dict):
        self.data = {} # lines data
        self.givens = {}
        self.junction_givens = {}
        data_values = data_dict.values()
        if (LineGrid.NODE_CHAR not in data_values and
            LineGrid.VERTICAL_CHAR not in data_values):
            self.translate_data_compact(data_dict)
            return
        # full representation with nodes and lines
        assert self.x_size % 2 == 1
        assert self.y_size % 2 == 1
        self.x_size = (self.x_size - 1) // 2
        self.y_size = (self.y_size - 1) // 2
        for pos in self.iter_checker():
            c = data_dict.get(pos)
            if c == LineGrid.VERTICAL_CHAR or c == LineGrid.HORIZONTAL_CHAR:
                self.data[pos] = BLACK
            elif c == self.CHARS[WHITE]:
                self.data[pos] = WHITE
            else:
                self.data[pos] = UNKNOWN
        # space givens
        for x in range(self.x_size):
            for y in range(self.y_size):
                pos = x, y
                x = x * 2 + 1
                y = y * 2 + 1
                c = data_dict.get((x, y))
                num = self.RCHARS.get(c)
                if num in GIVENS:
                    self.givens[pos] = num
        # junction givens
        for jx in range(self.x_size + 1):
            for jy in range(self.y_size + 1):
                pos = jx * 2, jy * 2
                c = data_dict.get(pos)
                if c is not None and c != LineGrid.NODE_CHAR:
                    self.junction_givens[(jx, jy)] = c

    def translate_data_compact(self, data_dict):
        for pos, value in data_dict.items():
            c = data_dict.get(pos)
            num = self.RCHARS.get(c)
            if num in GIVENS:
                self.givens[pos] = num
        for x, y in self.iter_checker():
            self.data[(x, y)] = UNKNOWN

    def __repr__(self):
        display_x_size = (self.x_size) * 2 + 1
        display_y_size = (self.y_size) * 2 + 1
        char_grid = [[' '] * display_x_size for i in range(display_y_size)]
        # place nodes
        for x in range(self.x_size + 1):
            for y in range(self.y_size + 1):
                char = self.junction_givens.get((x, y))
                if char is None:
                    char = LineGrid.NODE_CHAR
                char_grid[y * 2][x * 2] = char
        # show given numbers
        for key, value in self.givens.iteritems():
            x, y = key
            x = x * 2 + 1
            y = y * 2 + 1
            char_grid[y][x] = self.CHARS[value]
        # show lines
        for pos, color in self.data.items():
            x, y = pos
            if color == WHITE:
                char_grid[y][x] = self.CHARS[WHITE]
            elif color == BLACK:
                if LineGrid.is_vertical(pos):
                    char_grid[y][x] = LineGrid.VERTICAL_CHAR
                else:
                    char_grid[y][x] = LineGrid.HORIZONTAL_CHAR
        return '\n'.join(''.join(line) for line in char_grid)

    def is_vertical(position):
        x, y = position
        assert((x + y) % 2 == 1)
        return x % 2 == 0
    is_vertical = staticmethod(is_vertical)

    def iter_checker(self):
        for x in range(self.x_size * 2 + 1):
            for y in range(self.y_size * 2 + 1):
                if (x + y) % 2 == 1: # odd checkerboard pattern
                    yield (x, y)

    def adjacent_givens(self, position):
        x, y = position
        if LineGrid.is_vertical(position):
            givens = [(x-1, y), (x+1, y)]
        else: # horizontal
            givens = [(x, y-1), (x, y+1)]
        givens = [((gx - 1) // 2, (gy - 1) // 2) for gx, gy in givens]
        return self.cull_bounds_givens(givens)

    def precalc_junctions(self):
        self.junctions = []
        for x in range(self.x_size + 1):
            for y in range(self.y_size + 1):
                self.junctions.append((x, y))

    def precalc_junction_adjacencies(self):
        self.junction_adjacencies = {}
        for jpos in self.junctions:
            self.junction_adjacencies[jpos] = self._junction_adjacencies(jpos)
            
    def _junction_adjacencies(self, pos):
        x, y = pos
        x = x * 2
        y = y * 2
        return self.cull_bounds([(x-1, y),
                                 (x+1, y),
                                 (x, y-1),
                                 (x, y+1)])

    def cull_bounds_givens(self, position_list):
        return [pos for pos in position_list if pos in self.givens.keys()]


