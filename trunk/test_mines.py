import unittest
from constants import *
from mines import Mines

class TestMines(unittest.TestCase):
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

