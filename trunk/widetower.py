import board
from tritower import Tritower

class Widetower(Tritower):
    def valid_given_numbers(self):
        for pos in self.positions:
            number = self[pos]
            if number not in board.GIVENS:
                continue
            num_black = 0
            num_white = 0
            adjs = self.adjacencies[pos] + self.corner_adjacencies[pos]
            for adj in adjs:
                if self.is_black(adj):
                    num_black += 1
                elif self.is_white(adj):
                    num_white += 1
            if num_black > number or num_white > (len(adjs) - number):
                return False
        return True


import unittest

class TestWidetower(unittest.TestCase):
    def test_solve(self):
        test_boards = (
(
Widetower('''
   --2--
  -----4-  
  -2---3-  
   --3-2  
'''),
Widetower('''
   ..2X.   
  X..X.4X  
  .2X.X3.  
   ..3X2   
''')
),
(
Widetower('''
   2----   
  ---4--1  
  --5-4--  
   -2---   
'''),
Widetower('''
   2..X.   
  X.X4X.1  
  ..5X4..  
   X2..X   
''')
),
(
Widetower('''
   2----   
  -----4-  
  --4--3-  
   ---3-   
'''),
Widetower('''
   2.X.X   
  .X...4X  
  .X4.X3.  
   .X.3X   
''')
),
(
Widetower('''
   -1---
  -------
  ----4--
   --2--
'''),
Widetower('''
   .1...   
  X..X.X.  
  .X.X4.X  
   ..2..   
''')
),
(
Widetower('''
  *  -------
    2----45--
   ----------1 
   -2--------- 
    --3--3--- 
     -2----3
'''),
Widetower('''
  *  .X...X.     
    2X..X45X.    
   ..X...X.X.1   
   X2..X......   
    ..3X.3X.X    
     X2..X.3     
''')
),
)   
        for unsolved_board, solved_board in test_boards:
            unsolved_board.solve(3)
            self.assertEqual(unsolved_board, solved_board)

if __name__ == '__main__':
    unittest.main()
