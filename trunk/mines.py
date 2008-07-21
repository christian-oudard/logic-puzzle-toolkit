import board
from constants import GIVENS
from squaregrid import SquareGrid

class Mines(SquareGrid):
    def _is_valid(self):
        for pos in self.positions:
            number = self[pos]
            if number not in GIVENS:
                continue
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

