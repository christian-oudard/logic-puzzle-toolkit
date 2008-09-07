import valid
from squaregrid import SquareGrid

class Domino(SquareGrid):
    def valid_domino(self, position=None, color=None):
        for pos in self.black_positions:
            adjs = self.adjacencies[pos]
            if not valid.count_black(self, adjs, 1):
                return False
        return True

    def valid_black_tree(self):
        return True

    validity_checks = (
        valid.given_neighbors_corner,
        valid_domino,
        valid.white_edge_reachable,
        valid.black_connected_corner,
    )
