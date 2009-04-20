from constants import BLACK, WHITE
import valid
from utility import mdist
from linegrid import LineGrid

class SlitherLink(LineGrid):
    def valid_givens(self, position=None, color=None):
        if position:
            candidates = self.adjacent_givens(position)
        else:
            candidates = self.givens.keys()
        for gpos in candidates:
            number = self.givens[gpos]
            adjs = self.given_adjacencies[gpos]
            if not valid.count_black(self, adjs, number):
                return False
        return True

    def valid_junction(self, position=None, color=None):
        if position:
            x, y = position
            if self.is_vertical(position):
                adjacent_junctions = [(x, y-1), (x, y+1)]
            else:
                adjacent_junctions = [(x-1, y), (x+1, y)]
            candidates = [(x // 2, y // 2) for x, y in adjacent_junctions]
        else:
            candidates = self.junctions
        for jpos in candidates:
            adjs = self.junction_adjacencies[jpos]
            num_black = 0
            num_unknown = 0
            for adj in adjs:
                if self.is_black(adj):
                    num_black += 1
                elif self.is_unknown(adj):
                    num_unknown += 1
            if num_black >= 3 or (num_black == 1 and num_unknown == 0):
                return False
        return True

    validity_checks = (
        valid_givens,
        valid_junction,
        valid.black_connected,
    )

    conclusion_distance_values = {
        2: 4,
    }
    given_adjacent_values = {
        3: 2,
        2: .6,
        1: 3.2,
        0: 4,
    }
    conclusion_adjacent_value = 1.9
    known_adjacent_value = 1.2
    def priority(self, position):
        score = 0
        if self.last_conclusion is not None:
            if self.last_conclusion in self.adjacencies[position]:
                score += self.conclusion_adjacent_value
            else:
                dist = mdist(self.last_conclusion, position)
                if dist in self.conclusion_distance_values.keys():
                    score += self.conclusion_distance_values[dist]
        # known lines nearby
        adjs = self.adjacencies[position]
        known_score = self.known_adjacent_value * len(adjs)
        for adj in adjs:
            if self.is_unknown(adj):
                known_score -= self.known_adjacent_value
        score += known_score
        # givens nearby
        for gpos in self.adjacent_givens(position):
            number = self.givens[gpos]
            if number in self.given_adjacent_values.keys():
                score += self.given_adjacent_values[number]
        return score

