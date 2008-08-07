import board
from tritower import Tritower

class Widetower(Tritower):
    def valid_given_numbers(self):
        for pos in self.given_positions:
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

