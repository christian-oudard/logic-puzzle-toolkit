from copy import copy
def copy_board(board):
    new_board = copy(board)
    new_board.data = copy(board.data)
    new_board.positions = copy(board.positions)
    new_board.black_positions = copy(board.black_positions)
    new_board.white_positions = copy(board.white_positions)
    new_board.unknown_positions = copy(board.unknown_positions)
    return new_board

from constants import BLACK, WHITE
def opposite_color(color):
    if color == WHITE:
        return BLACK
    if color == BLACK:
        return WHITE

def mdist(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)
