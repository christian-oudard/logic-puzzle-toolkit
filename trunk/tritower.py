import board
from board import *
from trianglegrid import TriangleGrid

class Tritower(TriangleGrid):
    def is_valid(self):
        """Determine whether a board has a legal or illegal position."""
        return all((
            self.valid_tower_adjacency(),
            self.valid_given_numbers(),
            self.valid_white_triangles(),
            self.valid_tower_loops(),
            self.valid_towers_connected(),
        ))


    def valid_tower_adjacency(self):
        for pos in self.black_positions:
            for adj in self.adjacencies[pos]:
                if self.is_black(adj): # found a tower with another tower next to it
                    return False
        return True

    def valid_given_numbers(self):
        for pos in self.positions:
            number = self[pos]
            if number not in GIVENS:
                continue
            num_black = 0
            num_white = 0
            adjs = self.adjacencies[pos]
            for adj in adjs:
                if self.is_black(adj):
                    num_black += 1
                elif self.is_white(adj):
                    num_white += 1
            if num_black > number or num_white > (len(adjs) - number):
                return False
        return True


    def valid_white_triangles(self):
        # white triangles of size 2 are illegal
        for pos in self.white_positions: # consider every space and see if it is a center
            adjs = self.adjacencies[pos]
            if len(adjs) == 3: # must not be on the edge of the board
                if all(self.is_white(a) for a in adjs):
                    return False
        return True


    def valid_tower_loops(self):
        marks = {}
        for pos in self.white_positions.union(self.unknown_positions):
            marks[pos] = 'unvisited' # init marks

        def search_white(pos):
            marks[pos] = 'visited'
            adjs = self.adjacencies[pos]
            results = []
            for adj in adjs:
                if self.is_black(adj):
                    results.append(BLACK)
                elif marks[adj] == 'unvisited': # edge or unknown, and unvisited
                    results.append(search_white(adj))
            if len(adjs) < 3: # test this node for being an edge last, so whole group is still searched
                return 'edge'
            if any(r == 'edge' for r in results): # found a path to an edge
                return 'edge'
            return BLACK # no neighbor returned a path to an edge

        for pos in marks: # for every unvisited space
            if marks[pos] == 'unvisited':
                if search_white(pos) == BLACK:
                    return False

        return True


    def valid_towers_connected(self):
        # test that all towers are connected
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

