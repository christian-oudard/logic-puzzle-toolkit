from constants import GIVENS
from grid import Grid

class SpaceGrid(Grid):
    """
    Adds parsing of given numbers written in spaces.

    This class makes no semantic assumptions about what those given numbers might imply.
    """
    def __init__(self, data_string=''):
        Grid.__init__(self, data_string)
        self.precalc_corner_adjacency()

        # Add given number information.
        self.given_positions = set()
        for pos in self.positions:
            if self[pos] in GIVENS:
                self.given_positions.add(pos)

    def precalc_corner_adjacency(self):
        self.corner_adjacencies = {}
        self.both_adjacencies = {} # gives the union of adjacencies and corner_adjacencies
        for pos in self.positions:
            self.corner_adjacencies[pos] = self._corner_adjacencies(pos)
            self.both_adjacencies[pos] = self.adjacencies[pos] + self.corner_adjacencies[pos]

