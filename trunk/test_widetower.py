import unittest
from constants import BLACK, WHITE
from widetower import Widetower

class TestWidetower(unittest.TestCase):
    def test_valid_towers_connected_incremental(self):
        invalid_boards = [
            (
                Widetower('''
                          *X-2--
                          ....X4-
                          .2X..3-
                          *.X3X2
                          '''),
                (1, 0), BLACK
            ),
        ]
        for ib, position, color in invalid_boards:
            self.assertFalse(ib.valid_towers_connected())
            self.assertFalse(ib.valid_towers_connected(position, color))

    def test_solve(self):
        test_boards = (
            (
                Widetower('''
                          *--2--
                          -----4-  
                          -2---3-  
                          *--3-2  
                          '''),
                Widetower('''
                          *..2X.   
                          X..X.4X  
                          .2X.X3.  
                          *..3X2   
                          ''')
            ),
            (
                Widetower('''
                          *2----   
                          ---4--1  
                          --5-4--  
                          *-2---   
                          '''),
                Widetower('''
                          *2..X.   
                          X.X4X.1  
                          ..5X4..  
                          *X2..X   
                          ''')
            ),
            (
                Widetower('''
                          *2----   
                          -----4-  
                          --4--3-  
                          *---3-   
                          '''),
                Widetower('''
                          *2.X.X   
                          .X...4X  
                          .X4.X3.  
                          *.X.3X   
                          ''')
            ),
            (
                Widetower('''
                          *-1---
                          -------
                          ----4--
                          *--2--
                          '''),
                Widetower('''
                          *.1...   
                          X..X.X.  
                          .X.X4.X  
                          *..2..   
                          ''')
            ),
            (
                Widetower('''
                          ***-------
                          **2----45--
                          *----------1 
                          *-2--------- 
                          **--3--3--- 
                          ***-2----3
                          '''),
                Widetower('''
                          ***.X...X.     
                          **2X..X45X.    
                          *..X...X.X.1   
                          *X2..X......   
                          **..3X.3X.X    
                          ***X2..X.3     
                          ''')
            ),
        )   
        for unsolved_board, solved_board in test_boards:
            unsolved_board.solve(3)
            self.assertEqual(unsolved_board, solved_board)

