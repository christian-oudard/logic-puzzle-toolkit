import unittest
from nonogram import Nonogram, check_givens
from grid import Grid

class TestNonogram(unittest.TestCase):
    def setUp(self):
        self.valid_boards = (
            Nonogram('.', [()], [()]),
            Nonogram('X', [(1,)], [(1,)]),
            #Nonogram('-', [(1,)], [(1,)]),
        )
        self.invalid_boards = (
            Nonogram('X', [()], [()]),
        )
        self.test_boards = (
        )

    def test_bad_init(self):
        self.assertRaises(
            ValueError,
            lambda: Nonogram('XX', [(1,)], [()])
        )

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

    def test_check_givens(self):
        valid_cases = [
            ('.', ()),
            ('..', ()),
            ('X', (1,)),
            ('X.', (1,)),
            ('.X', (1,)),
            ('XX', (2,)),
            ('X.X', (1, 1)),
        ]
        invalid_cases = [
            ('.', (1,)),
            ('X', ()),
            ('X', (2,)),
            ('X.', (2,)),
            ('XX', (1,)),
            ('XX', (1, 1)),
            ('X.X', (3,)),
        ]
        def translate(cells):
            return [Grid.RCHARS[c] for c in cells]

        for cells, givens in valid_cases:
            self.assertTrue(check_givens(givens, translate(cells)))
        for cells, givens in invalid_cases:
            self.assertFalse(check_givens(givens, translate(cells)))
