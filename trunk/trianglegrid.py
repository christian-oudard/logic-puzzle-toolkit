import board
from grid import Grid

class TriangleGrid(Grid):
    def _adjacencies(self, pos):
        """Return all in-bounds adjacencies of the given position."""
        x, y = pos
        adjacency_list = [(x-1,y), (x+1,y)] # add left and right spaces

        if (x+y)%2 == 0: # even triangle, pointing down
            adjacency_list.append((x,y-1))
        else: # odd triangle, pointing up
            adjacency_list.append((x,y+1))

        return self._cull_bounds(adjacency_list)

    def _corner_adjacencies(self, pos):
        """Return all in-bounds corner-adjacencies of the given position."""
        x, y = pos
        # add 2-left, 2-right, and diagonal spaces
        adjacency_list = [(x-2,y), (x+2,y), (x-1,y-1),(x+1,y-1),(x-1,y+1),(x+1,y+1)]

        if (x+y)%2 == 0: # even triangle, pointing down
            adjacency_list.extend([(x,y+1),(x-2,y-1),(x+2,y-1)])
        else: # odd triangle, pointing up
            adjacency_list.extend([(x,y-1),(x-2,y+1),(x+2,y+1)])

        return self._cull_bounds(adjacency_list)


import unittest

class TestTriangleGrid(unittest.TestCase):
    def test_adjacencies(self):
        b = TriangleGrid('''
        ---
        ---''')
        for pos in b.positions:
            for adj in b.adjacencies[pos]:
                self.assert_(pos in b.adjacencies[adj])
                
    def test_corner_adjacencies(self):
        b = TriangleGrid('''
        ---
        ---''')
        for pos in b.positions:
            for adj in b.corner_adjacencies[pos]:
                self.assert_(pos in b.corner_adjacencies[adj])

if __name__ == '__main__':
    unittest.main()
    