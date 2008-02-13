from board import *
from trianglegrid import TriangleGrid

class Tritower(TriangleGrid):
    def is_valid(self):
        """Determine whether a board has a legal or illegal position."""
        return all((
            self.test_tower_adjacency(),
            self.test_given_numbers(),
            self.test_white_triangles(),
            self.test_tower_loops(),
            self.test_towers_connected(),
        ))


    def test_tower_adjacency(self):
        for pos in self.positions:
            if self.is_black(pos): # found a tower
                for adj in self.adjacencies[pos]:
                    if self.is_black(adj): # with another tower next to it
                        return False
        return True

    def test_given_numbers(self):
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


    def test_white_triangles(self):
        # white triangles of size 2 are illegal
        for pos in self.positions: # consider every space and see if it is a center
            if self.is_white(pos):
                adjs = self.adjacencies[pos]
                if len(adjs) == 3: # must not be on the edge of the board
                    if all(self.is_white(a) for a in adjs):
                        return False
        return True


    def test_tower_loops(self):
        marks = {}
        for pos in self.positions:
            if self.is_white(pos) or self.is_unknown(pos):
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

        for pos in self.positions: # for every unvisited space
            if pos in marks and marks[pos] == 'unvisited':
                if search_white(pos) == BLACK:
                    return False

        return True


    def test_towers_connected(self):
        # test that all towers are connected
        marks = {}
        for pos in self.positions:
            if self.is_black(pos) or self.is_unknown(pos):
                marks[pos] = 'unvisited' # init marks

        def search_black(pos): # just mark everything in the group 'visited'
            marks[pos] = 'visited'
            adjs = self.tower_adjacencies[pos]
            for adj in adjs:
                if adj in marks and marks[adj] == 'unvisited':
                    search_black(adj)

        group_count = 0
        for pos in self.positions: # for every unvisited tower
            if self.is_black(pos) and marks[pos] == 'unvisited': # don't start a group with an unknown space
                group_count += 1
                if group_count >= 2:
                    return False
                search_black(pos)

        return True

    def prioritized_positions(self):
        if solve_debug_display:
            print 'sort'
        priority_dic = {}
        for pos in self.positions:
            score = 0
            for adj in self.adjacencies[pos]:
                if self.is_black(adj): # priority up for being next to a tower
                    score += 1
                if self[adj] in GIVENS: # priority up for being next to a given
                    score += 1
                if self.is_white(adj): # priority up for being next to a known white space
                    score += 1            
            priority_dic[pos] = score
        return sorted(self.positions,key=priority_dic.__getitem__, reverse=True)
