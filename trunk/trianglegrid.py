import board
from constants import GIVENS # TEMP
from spacegrid import SpaceGrid

class TriangleGrid(SpaceGrid):
    def _adjacencies(self, pos):
        """Return all in-bounds adjacencies of the given position."""
        x, y = pos
        adjacency_list = [(x-1,y), (x+1,y)] # add left and right spaces

        if (x+y)%2 == 0: # even triangle, pointing down
            adjacency_list.append((x,y-1))
        else: # odd triangle, pointing up
            adjacency_list.append((x,y+1))

        return self.cull_bounds(adjacency_list)

    def _corner_adjacencies(self, pos):
        """Return all in-bounds corner-adjacencies of the given position."""
        x, y = pos
        # add 2-left, 2-right, and diagonal spaces
        adjacency_list = [(x-2,y), (x+2,y), (x-1,y-1),(x+1,y-1),(x-1,y+1),(x+1,y+1)]

        if (x+y)%2 == 0: # even triangle, pointing down
            adjacency_list.extend([(x,y+1),(x-2,y-1),(x+2,y-1)])
        else: # odd triangle, pointing up
            adjacency_list.extend([(x,y-1),(x-2,y+1),(x+2,y+1)])

        return self.cull_bounds(adjacency_list)

    # constants supplied by subclasses
    def priority(self, position):
        score = 0
        if self.last_conclusion in self.adjacencies[position]:
            score += self.conclusion_adjacent_value
        elif self.last_conclusion in self.corner_adjacencies[position]:
            score += self.conclusion_corner_adjacent_value
        for adj in self.adjacencies[position]:
            if self[adj] in GIVENS:
                score += self.given_adjacent_value
            elif self.is_black(adj) or self.is_white(adj):
                score += self.known_adjacent_value
        for adj in self.corner_adjacencies[position]:
            if self[adj] in GIVENS:
                score += self.given_corner_adjacent_value
            elif self.is_black(adj) or self.is_white(adj):
                score += self.known_corner_adjacent_value
        return score

    def is_edge(self, pos):
        adjs = self.adjacencies[pos]
        return len(adjs) < 3
