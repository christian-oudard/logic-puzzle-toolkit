from constants import *
from grid import Grid

class LineGrid(Grid):
    def __init__(self, data_string):
        Grid.__init__(self, data_string)

    def generate_positions(self):
        self.givens = self.data # data from data string only specifies givens
        self.data = {} # lines
        for x in range(self.x_size * 2 + 1):
            for y in range(self.y_size * 2 + 1):
                if (x + y) % 2 == 1: # odd checkerboard pattern
                    self.data[(x, y)] = UNKNOWN
        self.positions = set(self.data.keys())

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

    NODE_CHAR = '+'
    VERTICAL_CHAR = '|'
    HORIZONTAL_CHAR = '-'
    CHARS = Grid.CHARS
    CHARS[UNKNOWN] = ' '

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

