import valid
from constants import *
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

    def valid_towers_connected(self, position=None, color=None):
        if color == BLACK:
            if any(self.is_black(adj) for adj in self.corner_adjacencies[position]):
                return True
        if color == WHITE:
            if not any(self.is_black(adj) for adj in self.corner_adjacencies[position]):
                return True

        marks = {}
        for pos in self.black_positions.union(self.unknown_positions):
            marks[pos] = 'unvisited' # init marks

        def search_black(pos): # just mark everything in the group 'visited'
            marks[pos] = 'visited'
            adjs = self.corner_adjacencies[pos]
            for adj in adjs:
                if adj in marks and marks[adj] == 'unvisited':
                    search_black(adj)

        group_count = 0
        for pos in self.black_positions: # for every unvisited tower
            if marks[pos] == 'unvisited': # don't start a group with an unknown space
                group_count += 1
                if group_count >= 2:
                    return False
                search_black(pos)

        return True

    validity_checks = (
        valid.black_separate,
        valid.given_neighbors,
        valid_white_triangles,
        valid.white_edge_reachable,
        valid_towers_connected,
    )

    conclusion_adjacent_value = .8
    conclusion_corner_adjacent_value = 1.5
    given_adjacent_value = 3 
    given_corner_adjacent_value = .5
    known_adjacent_value = 2.1
    known_corner_adjacent_value = .4
