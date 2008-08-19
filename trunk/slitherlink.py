from constants import BLACK, WHITE
from utility import mdist
from linegrid import LineGrid

class SlitherLink(LineGrid):
    def __init__(self, data_string):
        LineGrid.__init__(self, data_string)
        self.precalc_junctions()
        self.precalc_junction_adjacencies()

    def is_valid(self, position=None, color=None):
        return all((
            self.valid_givens(position, color),
            self.valid_junction(position, color),
            self.valid_connected(position, color),
        ))

    def valid_givens(self, position=None, color=None):
        if position:
            candidates = self.adjacent_givens(position)
        else:
            candidates = self.givens.keys()
        for gpos in candidates:
            number = self.givens[gpos]
            adjs = self.given_adjacencies[gpos]
            num_black = 0
            num_white = 0
            for adj in adjs:
                if self.is_black(adj):
                    num_black += 1
                elif self.is_white(adj):
                    num_white += 1
            if num_black > number or num_white > (len(adjs) - number):
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

    def valid_connected(self, position=None, color=None):
        if position:
            next_to_black = any(self.is_black(adj) for adj in self.adjacencies[position])
            if color == BLACK and next_to_black:
                return True
            elif color == WHITE and not next_to_black:
                return True
        def search_black(pos): # just mark everything in the group 'visited'
            marks[pos] = 'visited'
            adjs = self.adjacencies[pos]
            for adj in adjs:
                if adj in marks and marks[adj] == 'unvisited':
                    search_black(adj)
        marks = {}
        for pos in self.black_positions.union(self.unknown_positions):
            marks[pos] = 'unvisited' # init marks
        group_count = 0
        for pos in self.black_positions:
            if marks[pos] == 'unvisited':
                group_count += 1
                if group_count >= 2:
                    return False
                search_black(pos)
        return True

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
                score += SlitherLink.conclusion_adjacent_value
            else:
                dist = mdist(self.last_conclusion, position)
                if dist in SlitherLink.conclusion_distance_values.keys():
                    score += SlitherLink.conclusion_distance_values[dist]
        # known lines nearby
        adjs = self.adjacencies[position]
        known_score = SlitherLink.known_adjacent_value * len(adjs)
        for adj in adjs:
            if self.is_unknown(adj):
                known_score -= SlitherLink.known_adjacent_value
        score += known_score
        # givens nearby
        for gpos in self.adjacent_givens(position):
            number = self.givens[gpos]
            if number in SlitherLink.given_adjacent_values.keys():
                score += SlitherLink.given_adjacent_values[number]
        return score

