import unittest
import valid
from constants import BLACK, WHITE
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
                     2-.
                     '''),
            Nurikabe('''
                     ---
                     X--
                     3--
                     '''),
            Nurikabe('''
                     ---
                     ..-
                     3--
                     '''),
            Nurikabe('''
                     X--
                     .X-
                     3--
                     '''),
            Nurikabe('''
                     2-.
                     '''),
            Nurikabe('''
                     --4
                     ..X
                     '''),
            Nurikabe('''
                     --4
                     -.X
                     '''),
            Nurikabe('''
                     .--.
                     6X.
                     '''),
            Nurikabe('''
                     XXXX
                     X..X
                     -.--
                     5X-
                     '''),
            Nurikabe('''
                     X-------------------X------X--------
                     --2X3X7---Xb-----2-X1X.---X1X-------
                     ----------4X-----XX1XXXX-.7X--9-----
                     ---5---X------X--.8XX..3X.XX--XX4---
                     ---X--X1X----X1X.-X..XXXXX1X-X2.XX--
                     X-X1XX1X--X-X1X..-X3X3X4.-X--3XXX1X-
                     X--X2-X--X1X6XXX.X3XX..X---------X--
                     ---------XX-.X1XXX..XXXX-------.----
                     --X-----X1X--XX...XXX...X3Xa--X8X---
                     -3X4-XX8-X--X1XX4XX1X.XXX.---X1X1X--
                     -X6XX.2X-----XX1XX1XX5X.XX---XXXX--7
                     --.--XXX4----X1XX1XX1X..X1X-X1X1X---
                     ---XX.4.XX----X-.XX.XXX4XX1X-X4X----
                     --X1X.XXX1X--X1X....--6X1XX3--.-X---
                     XX1XXX3..XX6--XXX9XXX--XX1X.--XX1X--
                     X.X...XXXX1XX--.4XX1X----X4X--4-X--5
                     X2XX..X1X.X2.X-.X2.X----X-.---------
                     -XX1X6XX..XXX1XXXXXX---X1XX-----X---
                     ---XXX1X.XX1XXX...X1X4-XXX3.---X1XX-
                     --5X.-X.6X1X3.XX4XXX--X1X6XXXX.-XX2X
                     --X4.-XXX.XX.X.XX1X.--XX...X.X4X1X.X
                     -------.X2X1XX..5XX-4-X..XXX.3XXX4XX
                     -X4---X.8XXXX1X.X-.-X-XXX5X1XXX.X..X
                     X3X--X1X.---6XXX-X4--2---.-XX1X3X.XX
                     X.X-.4XX--------..XXX---X----XX.XX3X
                     X.X--X-.-------XX4X2.X-.7X--.4XX.X.X
                     XX1XX1X--------.8X7XX--XX1XXXX1X.X.X
                     X.X2XX4---------XX..----4XX3X1XX3XXX
                     X2X.X..X5--------3X-----..X..X.2X2.X
                     XXXXX----------------------XXXXXXXXX
                     '''),
        ]
        for vb in valid_boards:
            self.assertTrue(vb.valid_white_groups(), 'This board should test valid:\n%s' % vb)

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
            Nurikabe('''
                     .X3-
                     XX--
                     '''),
            Nurikabe('''
                     .X3-
                     -X--
                     '''),
            Nurikabe('''
                     .--
                     .X-
                     3.-
                     '''),
            Nurikabe('''
                     .X.
                     .X-
                     3X-
                     '''),
        ]
        for ib in invalid_boards:
            self.assertFalse(ib.valid_white_groups(), 'This board should test invalid:\n%s' % ib)

    def test_valid_white_groups_incremental(self):
        invalid_boards = [
            (
                Nurikabe('''
                         .X.
                         .X.
                         3X.
                         '''),
                (2, 0), WHITE
            ),
            (
                Nurikabe('''
                         .XX
                         .X.
                         3X.
                         '''),
                (2, 2), WHITE
            ),
            (
                Nurikabe('''
                         2.X---X--2
                         XXX--X2X--
                         X2XX7X.X--
                         X.X.XXXX.-
                         XX.X..3X3-
                         .X2XXXX3XX
                         2XX4.X..X.
                         XX..XXXXX.
                         X1XXX.2X4.
                         '''),
                (3, 3), WHITE
            ),
            (
                Nurikabe('''
                         2.X---X.X2
                         XXX--X2XX.
                         X2X.7X.X.X
                         X.X-XXXX.X
                         XX.X..3X3X
                         .X2XXXX3XX
                         2XX4.X..X.
                         XX..XXXXX.
                         X1XXX.2X4.
                         '''),
                (7, 0), WHITE
            ),
        ]
        for ib, position, color in invalid_boards:
            self.assertFalse(ib.valid_white_groups())
            self.assertFalse(ib.valid_white_groups(position, color))

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
            self.assertTrue(valid.black_connected(vb))

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
            self.assertFalse(valid.black_connected(ib))

    def test_valid_black_connected_incremental(self):
        invalid_boards = [
            (
                Nurikabe('''
                         ---
                         -X.
                         3.X
                         '''),
                (1, 1), BLACK
            ),
            (
                Nurikabe('''
                         2.X------2
                         XXX---2---
                         X2X-7--X--
                         X.X----X.X
                         XX.X.-3X3X
                         .X2XXXX3XX
                         2XX4.X..X.
                         XX..XXXX..
                         X1XXX.2X4X
                         '''),
                (9, 8), BLACK
            ),
        ]
        for ib, position, color in invalid_boards:
            self.assertFalse(valid.black_connected(ib))
            self.assertFalse(valid.black_connected(ib, position, color))

    def test_solve(self):
        test_boards = [
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
#            (
#                Nurikabe('''
#                         2--------2
#                         ------2---
#                         -2--7-----
#                         ----------
#                         ------3-3-
#                         --2----3--
#                         2--4------
#                         ----------
#                         -1----2-4-
#                         '''),
#                Nurikabe('''
#                         2.X...XX.2
#                         XXX..X2XXX
#                         X2X.7X.X.X
#                         X.XXXXXX.X
#                         XX.X..3X3X
#                         .X2XXXX3XX
#                         2XX4.X..X.
#                         XX..XXXXX.
#                         X1XXX.2X4.
#                         ''')
#            ),
        ]
        for unsolved_board, solved_board in test_boards:
            unsolved_board.solve(2)
            self.assertEqual(unsolved_board, solved_board)

    def test_solve_incomplete(self):
        test_boards = [
            (Nurikabe('-2-'), Nurikabe('-2-')),
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
            (
                Nurikabe('''
                         ----
                         ----
                         ----
                         5-- 
                         '''),
                Nurikabe('''
                         XXXX
                         X..X
                         -.XX
                         5-X 
                         ''')
            ),
        ]
        for unsolved_board, solved_board in test_boards:
            unsolved_board.solve(2, True)
            self.assertEqual(unsolved_board, solved_board)

