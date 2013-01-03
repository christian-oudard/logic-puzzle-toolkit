from spacegrid import SpaceGrid

class SquareGrid(SpaceGrid):
    """
    Implements Moore neighborhood (orthogonal and diagonal) adjacency graph.
    """
    def _adjacencies(self, pos):
        x, y = pos
        return self.cull_bounds([(x-1, y),
                                 (x+1, y),
                                 (x, y-1),
                                 (x, y+1)])

    def _corner_adjacencies(self, pos):
        x, y = pos
        return self.cull_bounds([(x-1, y-1),
                                 (x-1, y+1),
                                 (x+1, y-1),
                                 (x+1, y+1)])

    def is_edge(self, pos):
        adjs = self.adjacencies[pos]
        return len(adjs) < 4
