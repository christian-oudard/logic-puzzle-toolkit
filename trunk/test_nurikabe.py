import unittest
from nurikabe import Nurikabe

class TestNurikabe(unittest.TestCase):
    def test_valid_no_black_2by2_pass(self):
        valid_boards = [
            Nurikabe('''
                     XX
                     X.
                     '''),
            Nurikabe('''
                     XX
                     X-
                     '''),
            Nurikabe('''
                     XXX
                     X-X
                     .X.
                     '''),
        ]   
        for vb in valid_boards:
            self.assertTrue(vb.valid_no_black_2by2())

    def test_valid_no_black_2by2_fail(self):
        invalid_boards = [
            Nurikabe('''
                     XX
                     XX''')
        ]
        for ib in invalid_boards:
            self.assertFalse(ib.valid_no_black_2by2())

    def test_valid_white_groups_pass(self):
        valid_boards = [
            Nurikabe('''
                     1-
                     --
                     '''),
            Nurikabe('''
                     .2
                     X-
                     '''),
            Nurikabe('''
                     3..
                     '''),
            Nurikabe('''
                     3.
                     -.
                     '''),
            Nurikabe('''
                     3-
                     '''),
            Nurikabe('''
                     2-
                     -.
                     '''),
            Nurikabe('''
                     .-.
                     '''),
            Nurikabe('''
                     2-.
                     '''),
        ]
        for vb in valid_boards:
            self.assertTrue(vb.valid_white_groups())

    def test_valid_white_groups_fail(self):
        invalid_boards = [
            Nurikabe('''
                     1.
                     '''),
            Nurikabe('''
                     3.3
                     '''),
            Nurikabe('''
                     2X
                     X-
                     '''),
            Nurikabe('''
                     2.
                     -.
                     '''),
            Nurikabe('''
                     3.
                     '''),
            Nurikabe('''
                     .
                     '''),
            Nurikabe('''
                     -X-
                     X.X
                     -X1
                     '''),
            Nurikabe('''
                     4.4
                     ---
                     '''),
        ]
        for ib in invalid_boards:
            self.assertFalse(ib.valid_white_groups())

    def test_valid_black_connected_pass(self):
        valid_boards = [
            Nurikabe('''
                     XXX
                     '''),
            Nurikabe('''
                     .X
                     '''),
            Nurikabe('''
                     X-X
                     '''),
        ]
        for vb in valid_boards:
            self.assertTrue(vb.valid_black_connected())

    def test_valid_black_connected_fail(self):
        invalid_boards = [
            Nurikabe('''
                     X.X
                     '''),
            Nurikabe('''
                     X..
                     .-X
                     '''),
            Nurikabe('''
                     1X
                     X.
                     '''),
        ]
        for ib in invalid_boards:
            self.assertFalse(ib.valid_black_connected())

    def test_solve(self):
        test_boards = (
            (Nurikabe('-2-'), Nurikabe('-2-')),
            (
                Nurikabe('''
                         a----------2-
                         '''),
                Nurikabe('''
                         a.........X2.
                         ''')
            ),
            (
                Nurikabe('''
                         ---
                         ---
                         3--
                         '''),
                Nurikabe('''
                         XXX
                         -.X
                         3-X
                         ''')
            ),
#            (
#                Nurikabe('''
#                         ----
#                         ----
#                         ----
#                         5-- 
#                         '''),
#                Nurikabe('''
#                         XXXX
#                         X..X
#                         -.XX
#                         5-X 
#                         ''')
#            ),
            (
                Nurikabe('''
                         -1-----
                         -------
                         2---3-3
                         ---1---
                         ----2--
                         -------
                         4-3---2
                         '''),
                Nurikabe('''
                         X1XXXX.
                         XXX..X.
                         2.XX3X3
                         XXX1XXX
                         ..XX2.X
                         .XX.XXX
                         4X3.X.2
                         ''')
            ),
            (
                Nurikabe('''
                         2--------2
                         ------2---
                         -2--7-----
                         ----------
                         ------3-3-
                         --2----3--
                         2--4------
                         ----------
                         -1----2-4-
                         '''),
                Nurikabe('''
                         2.X...XX.2
                         XXX..X2XXX
                         X2X.7X.X.X
                         X.XXXXXX.X
                         XX.X..3X3X
                         .X2XXXX3XX
                         2XX4.X..X.
                         XX..XXXXX.
                         X1XXX.2X4.
                         ''')
            ),
        )
        for unsolved_board, solved_board in test_boards:
            unsolved_board.solve(3)
            self.assertEqual(unsolved_board, solved_board)

