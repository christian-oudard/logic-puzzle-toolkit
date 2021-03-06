from board import *

class Grid(Board):
    """
    Implements basic parsing of strings into a dictionary of board positions.
    """

    # dictionaries to convert from constants to strings
    CHARS = {
        BLACK: 'X',
        WHITE: '.',
        UNKNOWN: '-',
        CONTRADICTION: '!',
        }
    for num in range(10):
        CHARS[num] = str(num) # digits 0 through 9
    for num in range(26):
        CHARS[num + 10] = chr(ord('a') + num) # a = 10 through z = 35
    RCHARS = {}
    for key, value in CHARS.iteritems():
        RCHARS[value] = key

    def __init__(self, data_string=''):
        Board.__init__(self)
        data_dict = self.grid_string_to_dict(data_string)
        self.translate_data(data_dict)
        self.precalc_positions()
        self.precalc_position_colors()
        self.precalc_adjacency()

    def precalc_positions(self):
        self.positions = set(self.data.keys())

    def precalc_position_colors(self):
        # positions by color
        self.black_positions = set()
        self.white_positions = set()
        self.unknown_positions = set()
        for pos in self.positions:
            self.update_color_caches(pos, self[pos])

    def precalc_adjacency(self):
        self.adjacencies = {}
        for pos in self.positions:
            self.adjacencies[pos] = self._adjacencies(pos)

    def translate_data(self, data_dict):
        self.data = {}
        for key, value in data_dict.items():
            x, y = key
            try:
                self.data[(x, y)] = self.RCHARS[value]
            except KeyError:
                pass # invalid characters are not included

    def cull_bounds(self, position_list):
        """Remove all positions that are out of bounds, and return the remainder."""
        return [pos for pos in position_list if pos in self.positions]

    def __repr__(self):
        char_grid = [[' '] * self.x_size for i in range(self.y_size)]
        for key, value in self.data.iteritems():
            x, y = key
            char_grid[y][x] = self.CHARS[value]
        return '\n'.join(''.join(line) for line in char_grid)

    def grid_string_to_dict(self, data_string):
        """
        Parse the string as a grid, and remove any extra whitespace around the border.
        """
        lines = data_string.split('\n')
        character_dict = {}
        for y, line in enumerate(lines):
            for x, character in enumerate(line):
                if not character.isspace():
                    character_dict[(x, y)] = character
        x_vals = []
        y_vals = []
        for pos in character_dict.keys():
            x, y = pos
            x_vals.append(x)
            y_vals.append(y)

        if not x_vals or not y_vals:
            self.x_size = self.y_size = 0
            return {}

        min_x, max_x = min(x_vals), max(x_vals)
        min_y, max_y = min(y_vals), max(y_vals)
        self.x_size = max_x - min_x + 1
        self.y_size = max_y - min_y + 1
        trimmed_dict = {}
        for key, value in character_dict.items():
            x, y = key
            trimmed_dict[(x-min_x, y-min_y)] = value
        return trimmed_dict
