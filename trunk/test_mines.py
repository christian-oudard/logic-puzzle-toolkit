import unittest
from mines import Mines

class TestMines(unittest.TestCase):
    def setUp(self):
        self.valid_boards = (
            Mines('X1'),
            Mines('.0.'),
            Mines('''
                  .1
                  1X'''),
        )
        self.invalid_boards = (
            Mines('X1X2-'),
            Mines('X1X2'),
        )
        self.unsolvable_boards = (
            Mines('''
                  -1
                  2-'''),
        )
        self.simple_boards = (
            (Mines('-'), Mines('-')),
            (Mines('---'), Mines('---')),
            (Mines('1-'), Mines('1X')),
            (Mines('-2-'), Mines('X2X')),
            (Mines('-1-2-1-'), Mines('.1X2X1.')),
            (Mines('1--'), Mines('1X-')),
        )
        self.complex_boards = (
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
        self.test_boards = self.simple_boards + self.complex_boards

    def test_is_valid_pass(self):
        for vb in self.valid_boards:
            self.assertTrue(vb.is_valid())

    def test_is_valid_fail(self):
        for ib in self.invalid_boards:
            self.assertFalse(ib.is_valid())

    def test_solve(self):
        for unsolved_board, solved_board in self.test_boards:
            unsolved_board.solve()
            self.assertEqual(unsolved_board, solved_board)

    def test_solve_minimum_required_depth(self):
        for unsolved_board, solved_board in self.complex_boards:
            unsolved_board.solve(3)
            self.assert_(unsolved_board.depth_reached <= 2)

    def test_solve_depth_limit(self):
        for unsolved_board, solved_board in self.simple_boards:
            for d in range(4):
                unsolved_board.solve(d)
                self.assert_(unsolved_board.depth_reached <= d)
            
    def test_contradiction(self):
        for ib in self.unsolvable_boards + self.invalid_boards:
            self.assertEqual(False, ib.solve())

    def test_already_solved(self):
        for sb in self.valid_boards:
            self.assertEqual(True, sb.solve())
