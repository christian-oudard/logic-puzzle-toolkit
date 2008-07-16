#! /usr/bin/env python

# test new solve function #
import unittest
from mines import Mines
from constants import *

class TestNewSolve(unittest.TestCase):
    def test_solve(self):
        test_boards = (
            (Mines('1-'), Mines('1X')),
            (Mines('-2-'), Mines('X2X')),
            (Mines('-1-2-1-'), Mines('.1X2X1.')),
            (Mines('1--'), Mines('1X-')),
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
        )
        for unsolved_board, solved_board in test_boards:
            unsolved_board.solve()
            self.assertEqual(unsolved_board, solved_board)

    def test_contradiction(self):
        invalid_boards = (
            Mines('X1X2-'),
            Mines('X1X2'),
            Mines('''
                  -1
                  2-'''),
        )
        for ib in invalid_boards:
            self.assertEqual(CONTRADICTION, ib.solve())
if __name__ == '__main__':
    import sys
    sys.argv.append('-v')
    unittest.main()
