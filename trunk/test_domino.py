import unittest
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

    def test_valid_black_tree_pass(self):
        valid_boards = [
            Domino('''
                   ...XX
                   .XX..
                   X..X.
                   X..X.
                   '''),
        ]   
        for vb in valid_boards:
            self.assertTrue(vb.valid_black_tree())

    def test_valid_black_tree_fail(self):
        invalid_boards = [
            Domino('''
                   .XX.
                   X..X
                   X..X
                   .XX.
                   '''),
            Domino('''
                   X.X
                   X.X
                   '''),
        ]
        for ib in invalid_boards:
            self.assertFalse(ib.valid_black_tree())
