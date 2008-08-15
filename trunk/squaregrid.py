from spacegrid import SpaceGrid

class SquareGrid(SpaceGrid):
    def _adjacencies(self, pos):
        x, y = pos
        return self._cull_bounds([(x-1, y),
                                  (x+1, y),
                                  (x, y-1),
                                  (x, y+1)])

    def _corner_adjacencies(self, pos):
        x, y = pos
        return self._cull_bounds([(x-1, y-1),
                                  (x-1, y+1),
                                  (x+1, y-1),
                                  (x+1, y+1)])
        
