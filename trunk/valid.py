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

def white_edge_reachable(board, position=None, color=None):
    if color == WHITE:
        return True
    marks = {}
    for pos in board.white_positions.union(board.unknown_positions):
        marks[pos] = 'unvisited'

    def search_white(pos):
        marks[pos] = 'visited'
        adjs = board.adjacencies[pos]
        results = []
        for adj in adjs:
            if board.is_black(adj):
                results.append(BLACK)
            elif marks[adj] == 'unvisited': # edge or unknown, and unvisited
                results.append(search_white(adj))
        if board.is_edge(pos): # test this node for being an edge last, so whole group is still searched
            return 'edge'
        if any(r == 'edge' for r in results): # found a path to an edge
            return 'edge'
        return BLACK # no neighbor returned a path to an edge

    for pos in marks: # for every unvisited space
        if marks[pos] == 'unvisited':
            if search_white(pos) == BLACK:
                return False

    return True

def search_connected_corner(self, searchable_color, position=None, color=None):
    #if position:
    #    next_to_black = any(self.is_black(adj) for adj in self.adjacencies[position])
    #    if color == BLACK and next_to_black:
    #        return True
    #    elif color == WHITE and not next_to_black:
    #        return True
    if searchable_color == WHITE:
        colored_positions = self.white_positions
    else:
        colored_positions = self.black_positions
    searchable_positions = colored_positions.union(self.unknown_positions)

    def search(pos):
        marks[pos] = 'visited'
        adjs = self.adjacencies[pos] + self.corner_adjacencies[pos]
        for adj in adjs:
            if adj in marks and marks[adj] == 'unvisited':
                search(adj)
    marks = {}
    for pos in searchable_positions:
        marks[pos] = 'unvisited' # init marks
    group_count = 0
    for pos in colored_positions:
        if marks[pos] == 'unvisited':
            group_count += 1
            if group_count >= 2:
                return False
            search(pos)
    return True

def white_connected_corner(self, position=None, color=None):
    return search_connected_corner(self, WHITE, position, color)

def black_connected_corner(self, position=None, color=None):
    return search_connected_corner(self, BLACK, position, color)

