import board
from tritower import Tritower

class Widetower(Tritower):
    def valid_given_numbers(self, position=None, color=None):
        candidates = self.given_positions
        if position:
            candidates = candidates.intersection(self.adjacencies[position] +
                                                 self.corner_adjacencies[position])
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

    # uses tritower's priority function, but changes some tuning parameters
    conclusion_adjacent_value = 1.3 
    conclusion_corner_adjacent_value = 2
    given_adjacent_value = 1.2 
    given_corner_adjacent_value = 0.1
    known_adjacent_value = 1.8 
    known_corner_adjacent_value = 0.1
