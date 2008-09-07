import unittest
import valid
from domino import Domino

class TestDomino(unittest.TestCase):
    def test_valid_domino_pass(self):
        valid_boards = [
            Domino('''
                   XX
                   ..
                   '''),
        ]   
        for vb in valid_boards:
            self.assertTrue(vb.is_valid())
            self.assertTrue(vb.valid_domino())

    def test_valid_domino_fail(self):
        invalid_boards = [
            Domino('''
                   X.
                   .X
                   '''),
            Domino('''
                   XX
                   .X
                   '''),
        ]
        for ib in invalid_boards:
            self.assertFalse(ib.valid_domino())

    def test_valid_white_edge_reachable_pass(self):
        valid_boards = [
            Domino('''
                   ...XX
                   .XX..
                   X..X.
                   X..X.
                   '''),
        ]   
        for vb in valid_boards:
            self.assertTrue(valid.white_edge_reachable(vb))

    def test_valid_white_edge_reachable_fail(self):
        invalid_boards = [
            Domino('''
                   .XX.
                   X..X
                   X..X
                   .XX.
                   '''),
        ]
        for ib in invalid_boards:
            self.assertFalse(valid.white_edge_reachable(ib))

    def test_valid_black_connected_pass(self):
        valid_boards = [
            Domino('''
                   ..XX
                   XX..
                   '''),
        ]   
        for vb in valid_boards:
            self.assertTrue(valid.black_connected_corner(vb))

    def test_valid_black_connected_fail(self):
        invalid_boards = [
            Domino('''
                   X.X
                   X.X
                   '''),
        ]
        for ib in invalid_boards:
            self.assertFalse(valid.black_connected_corner(ib))
