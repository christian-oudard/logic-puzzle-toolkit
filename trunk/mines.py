import board
from board import GIVENS
from squaregrid import SquareGrid

class Mines(SquareGrid):
    def is_valid(self):
        for pos in self.positions:
            number = self[pos]
            if number not in GIVENS:
                continue
            num_black = 0
            num_white = 0
            adjs = self.adjacencies[pos] + self.corner_adjacencies[pos]
            for adj in adjs:
                if self.is_black(adj):
                    num_black += 1
                elif self.is_white(adj):
                    num_white += 1
            if num_black > number or num_white > (len(adjs) - number):
                return False
        return True

import unittest

class TestMines(unittest.TestCase):
    def test_solve(self):
        test_boards = (
(
Mines('''
2---
--1-
-2--
---1'''),
Mines('''
2X..
X.1.
.2..
..X1''')
),
(
Mines('''
--2-3-
2-----
--24-3
1-34--
-----3
-3-3--'''),
Mines('''
X.2.3X
2X.XX.
..24X3
1.34X.
.XXX.3
X3.3XX''')
),
)
        #board.solve_debug_display = True
        for unsolved_board, solved_board in test_boards:
            unsolved_board.solve()
            self.assertEqual(unsolved_board, solved_board)

if __name__ == '__main__':
    unittest.main()    
