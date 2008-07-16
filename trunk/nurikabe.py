import board
from board import *
from squaregrid import SquareGrid

group_count = 0 # workaround until nonlocal keyword is available

class Nurikabe(SquareGrid):
    def _is_valid(self):
        return all((
            self.valid_white_groups(),
            self.valid_black_connected(),
            self.valid_no_black_2by2(),
        ))
    
    def valid_no_black_2by2(self):
        black_spaces = []
        for pos in self.positions:
            if self.is_black(pos):
                black_spaces.append(pos)
        for bs in black_spaces:
            x, y = bs
            square = [bs,
                      (x+1, y),
                      (x, y+1),
                      (x+1, y+1)]
            if all(s in black_spaces for s in square):
                return False
        return True
    
    def valid_white_groups(self):
        global group_count
        marks = {}
        for pos in self.positions:
            if self.is_white(pos):
                marks[pos] = 'unvisited' # initialize marks

        def search_white(pos):
            global group_count
            group_count += 1
            if marks[pos] == 'visited':
                return CONTRADICTION # found given numbers connected to each other
            marks[pos] = 'visited'
            adjs = self.adjacencies[pos]
            results = []
            for adj in adjs:
                if self.is_black(adj):
                    results.append(BLACK)
                elif self.is_unknown(adj):
                    results.append(UNKNOWN)
                elif marks[adj] == 'unvisited': # white, and unvisited
                    results.append(search_white(adj))
            if all(r == BLACK for r in results): # bordered by black
                return BLACK
            else: # reached an unknown
                return UNKNOWN
                
        # mark every numbered group visited, and check that the number is correct
        for pos in self.positions:
            number = self[pos]
            if number not in GIVENS:
                continue
            group_count = 0
            search_result = search_white(pos)
            if search_result == CONTRADICTION:
                return False
            if search_result == BLACK and group_count != number:
                return False
            elif search_result == UNKNOWN:
                if group_count > number:
                    return False

        # find orphan groups
        for pos in self.positions:
            if pos in marks and marks[pos] == 'unvisited':
                group_count = 0
                if search_white(pos) == BLACK:
                    return False # orphan group can't connect to a given number

        return True
    
    def valid_black_connected(self):
        marks = {}
        for pos in self.positions:
            if self.is_black(pos) or self.is_unknown(pos):
                marks[pos] = 'unvisited' # init marks

        def search_black(pos): # just mark everything in the group 'visited'
            marks[pos] = 'visited'
            adjs = self.adjacencies[pos]
            for adj in adjs:
                if adj in marks and marks[adj] == 'unvisited':
                    search_black(adj)

        group_count = 0
        for pos in self.positions: # for every unvisited tower
            if self.is_black(pos) and marks[pos] == 'unvisited': # don't start a group with an unknown space
                group_count += 1
                if group_count >= 2:
                    return False
                search_black(pos)

        return True


import unittest    
    
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
a----------2-
'''),
Nurikabe('''
a.........X2.
''')
),
)
        for unsolved_board, solved_board in test_boards:
            unsolved_board.solve()
            self.assertEqual(unsolved_board, solved_board)

if __name__ == '__main__':
    import sys
    sys.argv.append('-v')
    unittest.main()
    
