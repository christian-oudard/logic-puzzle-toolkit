from constants import *
from grid import Grid

class LineGrid(Grid):
    def __init__(self, data_string):
        Grid.__init__(self, data_string)
        self.precalc_given_adjacencies()

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
        return self._cull_bounds(adjacencies)

    def _given_adjacencies(self, given_pos):
        x, y = given_pos
        x = x * 2 + 1
        y = y * 2 + 1
        return self._cull_bounds([(x-1, y),
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
        if data_dict[(0, 0)] == LineGrid.NODE_CHAR:
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
            # givens
            for x in range(self.x_size):
                for y in range(self.y_size):
                    pos = x, y
                    x = x * 2 + 1
                    y = y * 2 + 1
                    c = data_dict.get((x, y))
                    num = self.RCHARS.get(c)
                    if num in GIVENS:
                        self.givens[pos] = num
        else:
            # compact representation, no lines
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
                char_grid[y * 2][x * 2] = self.NODE_CHAR
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

