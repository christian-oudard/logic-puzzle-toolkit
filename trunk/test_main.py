#! /usr/bin/env python

from tritower import Tritower

import unittest

class TestTritower(unittest.TestCase):
    def test_adjacencies(self):
        b = Tritower(3)
        for pos in b.positions:
            for adj in b.adjacencies[pos]:
                self.assert_(pos in b.adjacencies[adj])
                
    def test_tower_adjacencies(self):
        b = Tritower(3)
        for pos in b.positions:
            for adj in b.tower_adjacencies[pos]:
                self.assert_(pos in b.tower_adjacencies[adj])

    def test_is_valid(self):
        valid_boards = [
Tritower('''
 1  
    
'''),
Tritower('''
 1. 
    
'''),
Tritower('''
 0. 
 .  
'''),
Tritower('''
    
  X 
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
  X.. .X.
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
 1X 
 X  
'''),
Tritower('''
 XX.
 .X.
'''),
Tritower('''
   .   .
  . .2. .
  .     .
   .   .
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
        for board in valid_boards:
            self.assertTrue(board.is_valid())
        for board in invalid_boards:
            self.assertFalse(board.is_valid())

    def test_solve(self):
        boards = (
(
Tritower('''
    2  0
     1   
   1     
      1 
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
    1   
      2 1
    2    
       0
'''),
Tritower('''
   X1.X.
  ..X.2X1
  .X2.X..
   .X..0
''')
),
#(
#Tritower('''
            
       #2 1  1
    #21    2   
              
             
      #1   0 
#'''),
#Tritower('''
     #..X..X.
    #X..2X1.X1
   #X21X..X2X. 
   #...X...... 
    #X...X.X. 
     #X1.X.0.
#'''),
#),
#(
#Tritower('''
                
                 
     #0            
                   
        #1          
            #1 2  1
       #2  2      
        #1 1  2  
#'''),
#Tritower('''
       #..X...X..
      #X....X....X
     #0..X..X..X...
    #..X.X...X.X..X.
    #X...1.X......X.
     #..X..X.1X2X.1
      #X2.X2..X..X
       #X1.1X.2X.
#'''),
#),
)
        for board, solved_board in boards:
            board.solve()
            self.assertEqual(board, solved_board)

if __name__ == '__main__':
    unittest.main()