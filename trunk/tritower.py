import valid
from constants import BLACK
from trianglegrid import TriangleGrid

class Tritower(TriangleGrid):
    def valid_white_triangles(self, position=None, color=None):
        # white triangles of size 2 are illegal
        if color == BLACK:
            return True
        candidates = self.white_positions
        if position:
            candidates = candidates.intersection([position] +
                                                 self.adjacencies[position])
        for pos in candidates: # consider every space and see if it is a center
            adjs = self.adjacencies[pos]
            if len(adjs) == 3: # must not be on the edge of the board
                if all(self.is_white(a) for a in adjs):
                    return False
        return True

    validity_checks = (
        valid.black_separate,
        valid.given_neighbors,
        valid_white_triangles,
        valid.white_edge_reachable,
        valid.black_connected_corner,
    )

    conclusion_adjacent_value = .8
    conclusion_corner_adjacent_value = 1.5
    given_adjacent_value = 3 
    given_corner_adjacent_value = .5
    known_adjacent_value = 2.1
    known_corner_adjacent_value = .4
