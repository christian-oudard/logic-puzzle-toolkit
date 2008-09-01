# validity checking functions
#TODO: these are no longer member functions, replace self with board
#TODO: given_neighbors and given_neighbors_corner have duplication

from constants import *

def given_neighbors(self, position=None, color=None):
    """Each given number specifies the number of black neighbors."""
    candidates = self.given_positions
    if position:
        candidates = candidates.intersection(self.adjacencies[position])
    for pos in candidates:
        number = self[pos]
        num_black = 0
        num_white = 0
        adjs = self.adjacencies[pos]
        for adj in adjs:
            if self.is_black(adj):
                num_black += 1
            elif self.is_white(adj):
                num_white += 1
        if num_black > number or num_white > (len(adjs) - number):
            return False
    return True

def given_neighbors_corner(self, position=None, color=None):
    """Each given number specifies the number of black neighbors, including diagonally."""
    candidates = self.given_positions
    if position:
        adjacencies = set(self.adjacencies[position] +
                         self.corner_adjacencies[position])
        candidates = candidates.intersection(adjacencies)
    for pos in candidates:
        number = self[pos]
        num_black = 0
        num_white = 0
        adjs = self.adjacencies[pos] + self.corner_adjacencies[pos]
        for adj in adjs:
            if self.is_black(adj):
                num_black += 1
            elif self.is_white(adj):
                num_white += 1
        if num_black > number or num_white > (len(adjs) - number):
            return False
    return True

def black_separate(self, position=None, color=None):
    """Black spaces may not be adjacent to each other."""
    if color == WHITE:
        return True
    if position and color == BLACK:
        for adj in self.adjacencies[position]:
            if self.is_black(adj):
                return False
    for pos in self.black_positions:
        for adj in self.adjacencies[pos]:
            if self.is_black(adj): # found a tower with another tower next to it
                return False
    return True
