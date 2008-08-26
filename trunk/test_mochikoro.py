import unittest
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
        ]   
        for vb in valid_boards:
            self.assertTrue(vb.valid_white_rectangles(), 'board tested invalid:\n%r' % vb)

    def test_valid_white_rectangles_fail(self):
        invalid_boards = [
            Mochikoro('''
                     X.
                     ..''')
        ]
        for ib in invalid_boards:
            self.assertFalse(ib.valid_white_rectangles(), 'board tested valid:\n%r' % ib)

    def test_valid_white_corner_connected_pass(self):
        valid_boards = [
            Mochikoro('''
                      X.
                      .X
                      '''),
        ]   
        for vb in valid_boards:
            self.assertTrue(vb.valid_white_corner_connected(), 'board tested invalid:\n%r' % vb)

    def test_valid_white_corner_connected_fail(self):
        invalid_boards = [
            Mochikoro('''
                      XX.
                      .X.
                      ''')
        ]
        for ib in invalid_boards:
            self.assertFalse(ib.valid_white_corner_connected(), 'board tested valid:\n%r' % ib)

