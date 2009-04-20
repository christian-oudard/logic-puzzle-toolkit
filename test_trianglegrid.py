import unittest
from trianglegrid import TriangleGrid

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


