import unittest
import valid
from mochikoro import Mochikoro

class TestMochikoro(unittest.TestCase):
    def test_valid_white_rectangles_pass(self):
        valid_boards = [
            Mochikoro('''
                     XX
                     ..
                     '''),
            Mochikoro('''
                     X-
                     ..
                     '''),
            Mochikoro('''
                     .-
                     ..
                     '''),
            # last space considered is unknown
            Mochikoro('''
                     ..
                     .-
                     '''),
        ]   
        for vb in valid_boards:
            self.assertTrue(vb.valid_white_rectangles(), 'board tested invalid:\n%r' % vb)

    def test_valid_white_rectangles_fail(self):
        invalid_boards = [
            Mochikoro('''
                      X.
                      ..
                      '''),
            Mochikoro('''
                      X.
                      3.
                      ''')
        ]
        for ib in invalid_boards:
            self.assertFalse(ib.valid_white_rectangles(), 'board tested valid:\n%r' % ib)

    def test_valid_white_connected_both_pass(self):
        valid_boards = [
            Mochikoro('''
                      X.
                      .X
                      '''),
        ]   
        for vb in valid_boards:
            self.assertTrue(valid.white_connected_both(vb), 'board tested invalid:\n%r' % vb)

    def test_valid_white_connected_both_fail(self):
        invalid_boards = [
            Mochikoro('''
                      XX.
                      .X.
                      '''),
            Mochikoro('''
                      .X..3
                      2XXXX
                      XX.2X
                      ..XXX
                      4.X1X
                      '''),
        ]
        for ib in invalid_boards:
            self.assertFalse(valid.white_connected_both(ib), 'board tested valid:\n%r' % ib)

    def test_solve(self):
        test_boards = [
            (
                Mochikoro('''
                          ----3
                          2----
                          ---2-
                          -----
                          4--1-
                          '''),
                Mochikoro('''
                          XX..3
                          2.XXX
                          XX.2X
                          ..XX.
                          4.X1X
                          ''')
            )
        ]
        for unsolved_board, solved_board in test_boards:
            unsolved_board.solve()
            self.assertEqual(unsolved_board, solved_board)
