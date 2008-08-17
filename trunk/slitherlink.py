from utility import mdist
from linegrid import LineGrid

class SlitherLink(LineGrid):
    def __init__(self, data_string):
        LineGrid.__init__(self, data_string)
        self.precalc_junctions()
        self.precalc_junction_adjacencies()

    def is_valid(self, position=None, color=None):
        return all((
            self.valid_givens(),
            self.valid_junction(),
        ))

    def valid_givens(self):
        for gpos, number in self.givens.items():
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

    def valid_junction(self):
        for jpos in self.junctions:
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

    conclusion_distance_values = {
        2: .5,
        4: .2,
    }
    given_adjacent_values = {
        3: 2,
        2: .5,
        1: 1,
        0: 3,
    }
    conclusion_adjacent_value = 3
    known_adjacent_value = 0
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
        for adj in self.adjacencies[position]:
            if not self.is_unknown(adj):
                score += SlitherLink.known_adjacent_value
        # givens nearby
        x, y = position
        if LineGrid.is_vertical(position):
            givens = [(x-1, y), (x+1, y)]
        else: # horizontal
            givens = [(x, y-1), (x, y+1)]
        for gx, gy in givens:
            gx = (gx - 1) // 2
            gy = (gy - 1) // 2
            number = self.givens.get((gx, gy))
            if number in SlitherLink.given_adjacent_values.keys():
                score += SlitherLink.given_adjacent_values[number]
        return score

    def precalc_junctions(self):
        self.junctions = []
        for x in range(self.x_size + 1):
            for y in range(self.y_size + 1):
                self.junctions.append((x, y))

    def precalc_junction_adjacencies(self):
        self.junction_adjacencies = {}
        for jpos in self.junctions:
            self.junction_adjacencies[jpos] = self._junction_adjacencies(jpos)
            
    def _junction_adjacencies(self, pos):
        x, y = pos
        x = x * 2
        y = y * 2
        return self._cull_bounds([(x-1, y),
                                  (x+1, y),
                                  (x, y-1),
                                  (x, y+1)])



