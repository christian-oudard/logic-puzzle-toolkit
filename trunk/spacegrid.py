from constants import GIVENS
from grid import Grid

class SpaceGrid(Grid):
    def __init__(self, data_string):
        Grid.__init__(self, data_string)
        self.precalc_corner_adjacency()
        self.given_positions = set()
        for pos in self.positions:
            if self[pos] in GIVENS:
                self.given_positions.add(pos)

    def precalc_corner_adjacency(self):
        self.corner_adjacencies = {}
        for pos in self.positions:
            self.corner_adjacencies[pos] = self._corner_adjacencies(pos)
