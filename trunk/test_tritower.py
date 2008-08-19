import unittest
from tritower import Tritower

class TestTritower(unittest.TestCase):
    def test_is_valid_pass(self):
        valid_boards = [
            Tritower('''
                     -1-
                     ---
                     '''),
            Tritower('''
                     -1.
                     ---
                     '''),
            Tritower('''
                     -0.
                     -.-
                     '''),
            Tritower('''
                     ---
                     -X-
                     '''),
            Tritower('''
                     ...
                     .X.
                     '''),
            Tritower('''
                     *..X.. 
                     .X....X
                     .X..X..
                     *..X.. 
                     '''),
            Tritower('''
                     *.X... 
                     ..X..X.
                     ...X.X.
                     *X.... 
                     '''),
            Tritower('''
                     *.X... 
                     ..X..X.
                     X..-.X.
                     *..X..
                     '''),
            Tritower('''
                     *..X..
                     .X...-.
                     .X..X..
                     *..X..
                     '''),
        ]   
        for vb in valid_boards:
            self.assertTrue(vb.is_valid())

    def test_is_valid_fail(self):
        invalid_boards = [
            Tritower('''
                     -1X 
                     -X- 
                     '''),
            Tritower('''
                     XX.
                     .X.
                     '''),
            Tritower('''
                     *-----
                     --.2.--
                     -------
                     *-----
                     '''),
            Tritower('''
                     *..X..
                     .X.....
                     .X..X..
                     *..X..
                     '''),
            Tritower('''
                     *..X..
                     ..X..X.
                     .X...X.
                     *..X..
                     '''),
            Tritower('''
                     *.X...
                     ..X..X.
                     X....X.
                     *..X..
                     '''),
        ]   
        for ib in invalid_boards:
            self.assertFalse(ib.is_valid())

    def test_is_valid_triangles_incremental(self):
        b = Tritower('''
                     X.X
                     ...
                     ''')
        self.assertFalse(b.valid_white_triangles())
        self.assertFalse(b.valid_white_triangles((1, 1)))

    def test_solve(self):
        test_boards = (
            (Tritower('-'), Tritower('-')),
            (
                Tritower('''
                         *-2--0
                         ---1---
                         -1-----
                         *---1-
                         '''),
                Tritower('''
                         *X2X.0
                         X..1..X
                         .1X.X..
                         *.X.1X
                         '''),
            ),
            (
                Tritower('''
                         *-1---
                         ----2-1
                         --2----
                         *----0
                         '''),
                Tritower('''
                         *X1.X.
                         ..X.2X1
                         .X2.X..
                         *.X..0
                         ''')
            ),
#            (
#                Tritower('''
#                         ***---------
#                         **-----------
#                         *0------------
#                         ---------------
#                         ----1----------
#                         *-------1-2--1
#                         **-2--2------
#                         ***-1-1--2--
#                         '''),
#                Tritower('''
#                         ***..X...X..
#                         **X....X....X
#                         *0..X..X..X...
#                         ..X.X...X.X..X.
#                         X...1.X......X.
#                         *..X..X.1X2X.1
#                         **X2.X2..X..X
#                         ***X1.1X.2X.
#                         '''),
#            ),
        )
        for unsolved_board, solved_board in test_boards:
            unsolved_board.solve()
            self.assertEqual(unsolved_board, solved_board)

    def test_solve_incomplete(self):
        test_boards = [
            (
                Tritower('''
                         ***-------
                         **---2-1--1
                         *-21----2---
                         *-----------
                         **---------
                         ***-1---0-
                         '''),
                Tritower('''
                         ***..X..X.
                         **X..2X1.X1
                         *X21X..X2X.-
                         *...X......-
                         **X...X.X.-
                         ***X1.X.0.
                         '''),
            ),
        ]
        for unsolved_board, solved_board in test_boards:
            unsolved_board.solve(1, True)
            self.assertEqual(unsolved_board, solved_board)
