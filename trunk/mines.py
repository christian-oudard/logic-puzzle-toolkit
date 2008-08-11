import board
from constants import GIVENS
from squaregrid import SquareGrid

class Mines(SquareGrid):
    def is_valid(self, position=None, color=None):
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

