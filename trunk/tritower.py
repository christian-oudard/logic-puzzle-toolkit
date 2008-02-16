import board
from board import *
from trianglegrid import TriangleGrid

class Tritower(TriangleGrid):
    def is_valid(self):
        """Determine whether a board has a legal or illegal position."""
        return all((
            self.valid_tower_adjacency(),
            self.valid_given_numbers(),
            self.valid_white_triangles(),
            self.valid_tower_loops(),
            self.valid_towers_connected(),
        ))


    def valid_tower_adjacency(self):
        for pos in self.positions:
            if self.is_black(pos): # found a tower
                for adj in self.adjacencies[pos]:
                    if self.is_black(adj): # with another tower next to it
                        return False
        return True

    def valid_given_numbers(self):
        for pos in self.positions:
            number = self[pos]
            if number not in GIVENS:
                continue
            num_black = 0
            num_white = 0
            adjs = self.adjacencies[pos]
            for adj in adjs:
                if self.is_black(adj):
                    num_black += 1
                elif self.is_white(adj):
                    num_white += 1
            if num_black > number or num_white > (len(adjs) - number):
                return False
        return True


    def valid_white_triangles(self):
        # white triangles of size 2 are illegal
        for pos in self.positions: # consider every space and see if it is a center
            if self.is_white(pos):
                adjs = self.adjacencies[pos]
                if len(adjs) == 3: # must not be on the edge of the board
                    if all(self.is_white(a) for a in adjs):
                        return False
        return True


    def valid_tower_loops(self):
        marks = {}
        for pos in self.positions:
            if self.is_white(pos) or self.is_unknown(pos):
                marks[pos] = 'unvisited' # init marks

        def search_white(pos):
            marks[pos] = 'visited'
            adjs = self.adjacencies[pos]
            results = []
            for adj in adjs:
                if self.is_black(adj):
                    results.append(BLACK)
                elif marks[adj] == 'unvisited': # edge or unknown, and unvisited
                    results.append(search_white(adj))
            if len(adjs) < 3: # test this node for being an edge last, so whole group is still searched
                return 'edge'
            if any(r == 'edge' for r in results): # found a path to an edge
                return 'edge'
            return BLACK # no neighbor returned a path to an edge

        for pos in self.positions: # for every unvisited space
            if pos in marks and marks[pos] == 'unvisited':
                if search_white(pos) == BLACK:
                    return False

        return True


    def valid_towers_connected(self):
        # test that all towers are connected
        marks = {}
        for pos in self.positions:
            if self.is_black(pos) or self.is_unknown(pos):
                marks[pos] = 'unvisited' # init marks

        def search_black(pos): # just mark everything in the group 'visited'
            marks[pos] = 'visited'
            adjs = self.corner_adjacencies[pos]
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

class TestTritower(unittest.TestCase):
    def test_is_valid(self):
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
 ..X.. 
.X....X
.X..X..
 ..X.. 
'''),
Tritower('''
 .X... 
..X..X.
...X.X.
 X.... 
'''),
Tritower('''
 .X... 
..X..X.
X..-.X.
 ..X..
'''),
Tritower('''
 ..X..
.X... .
.X..X..
 ..X..
'''),
]   
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
 -----
--.2.--
-------
 -----
'''),
Tritower('''
 ..X..
.X.....
.X..X..
 ..X..
'''),
Tritower('''
 ..X..
..X..X.
.X...X.
 ..X..
'''),
Tritower('''
 .X...
..X..X.
X....X.
 ..X..
'''),
]   
        for vb in valid_boards:
            self.assertTrue(vb.is_valid())
        for ib in invalid_boards:
            self.assertFalse(ib.is_valid())

    def test_solve(self):
        test_boards = (
(
Tritower('''
 -2--0
---1---
-1-----
 ---1-
'''),
Tritower('''
 X2X.0
X..1..X
.1X.X..
 .X.1X
'''),
),
(
Tritower('''
 -1---
----2-1
--2----
 ----0
'''),
Tritower('''
 X1.X.
..X.2X1
.X2.X..
 .X..0
''')
),
(
Tritower('''
*  -------
  ---2-1--1
 -21----2---
 -----------
  ---------
   -1---0-
'''),
Tritower('''
*  ..X..X.
  X..2X1.X1
 X21X..X2X.-
 ...X......-
  X...X.X.-
   X1.X.0.
'''),
),
(
Tritower('''
   ---------
  -----------
 0------------
---------------
----1----------
 -------1-2--1
  -2--2------
   -1-1--2--
'''),
Tritower('''
   ..X...X..
  X....X....X
 0..X..X..X...
..X.X...X.X..X.
X...1.X......X.
 ..X..X.1X2X.1
  X2.X2..X..X
   X1.1X.2X.
'''),
),
)
        #board.solve_debug_display = True
        for unsolved_board, solved_board in test_boards:
            unsolved_board.solve()
            self.assertEqual(unsolved_board, solved_board)

if __name__ == '__main__':
    unittest.main()
    