# validity checking functions

from constants import *

def count_black(board, positions, number):
    """The number of black spaces among a set of positions must match the given number."""
    num_black = 0
    num_white = 0
    for pos in positions:
        if board.is_black(pos):
            num_black += 1
        elif board.is_white(pos):
            num_white += 1
    if num_black > number or num_white > (len(positions) - number):
        return False
    return True


def given_neighbors(board, position=None, color=None):
    """Each given number specifies the number of black neighbors."""
    candidates = board.given_positions
    if position:
        candidates = candidates.intersection(board.adjacencies[position])
    for pos in candidates:
        number = board[pos]
        adjs = board.adjacencies[pos]
        if not count_black(board, adjs, number):
            return False
    return True

def given_neighbors_corner(board, position=None, color=None):
    """Each given number specifies the number of black neighbors, including diagonally."""
    candidates = board.given_positions
    if position:
        adjacencies = set(board.adjacencies[position] +
                         board.corner_adjacencies[position])
        candidates = candidates.intersection(adjacencies)
    for pos in candidates:
        adjs = board.adjacencies[pos] + board.corner_adjacencies[pos]
        number = board[pos]
        if not count_black(board, adjs, number):
            return False
    return True

def black_separate(board, position=None, color=None):
    """Black spaces may not be adjacent to each other."""
    if color == WHITE:
        return True
    if position and color == BLACK:
        for adj in board.adjacencies[position]:
            if board.is_black(adj):
                return False
    for pos in board.black_positions:
        for adj in board.adjacencies[pos]:
            if board.is_black(adj): # found a tower with another tower next to it
                return False
    return True
