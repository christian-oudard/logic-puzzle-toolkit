from constants import WHITE, BLACK
from board import opposite_color
from grid import Grid

class Nonogram(Grid):
    def __init__(self, data_string='', column_givens=None, row_givens=None):
        Grid.__init__(self, data_string)

        if column_givens is None:
            column_givens = []
        if row_givens is None:
            row_givens = []
        self.column_givens = column_givens
        self.row_givens = row_givens

        if len(column_givens) != self.x_size:
            raise ValueError('Incorrect number of column givens.')
        if len(row_givens) != self.y_size:
            raise ValueError('Incorrect number of row givens.')



    def valid_nonogram(self, position=None, color=None):
        for x in range(self.x_size):
            column = [self[(x, y)] for y in range(self.y_size)]
            if not check_givens(self.column_givens[x], column):
                return False
        for y in range(self.y_size):
            row = [self[(x, y)] for x in range(self.x_size)]
            if not check_givens(self.row_givens[y], row):
                return False
        return True

    validity_checks = (
        valid_nonogram,
    )


def check_givens(givens, cells):
    # The "cells" argument can be either a horizontal row or a vertical column.

    # The edges of the board count as white.
    cells = [WHITE] + cells + [WHITE]

    # Find existing ranges, and make sure that they exist, in order, in the
    # list of given ranges.
    found_ranges = []
    current_size = None
    # Iterate pairwise.
    for previous_color, current_color in zip(cells[:-1], cells[1:]):
        #if current_color == UNKNOWN:
        #    # Cancel whatever range we were doing.
        #    current_size = None
        if previous_color == WHITE and current_color == BLACK:
            # Start a range.
            current_size = 1
        elif previous_color == BLACK and current_color == BLACK:
            # Continue the current range.
            current_size += 1
        elif previous_color == BLACK and current_color == WHITE:
            # Finish the range.
            found_ranges.append(current_size)
            current_size = None
    if found_ranges != list(givens):
        return False
    return True
