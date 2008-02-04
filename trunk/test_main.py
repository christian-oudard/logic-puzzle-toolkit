#! /usr/bin/env python

import board
from board import *

def test_solve():
    boards = (
(
Board('''
    2  0
     1   
   1     
      1 
'''),
Board('''
   X2X.0
  X..1..X
  .1X.X..
   .X.1X
'''),
),
(
Board('''
    1   
      2 1
    2    
       0
'''),
Board('''
   X1.X.
  ..X.2X1
  .X2.X..
   .X..0
''')
),
(
Board('''
            
       2 1  1
    21    2   
              
             
      1   0 
'''),
Board('''
     ..X..X.
    X..2X1.X1
   X21X..X2X. 
   ...X...... 
    X...X.X. 
     X1.X.0.
'''),
),
#(
#Board('''
#                
#                 
#     0            
#                   
#        1          
#            1 2  1
#       2  2      
#        1 1  2  
#'''),
#Board() 
#),
)
    for board, solved_board in boards:
        if board is not None and solved_board is not None:
            steps = board.solve()
            print steps
            if board != solved_board:
                return False
    return True
            

def test_tower_adjacencies():
    b = Board(2)
#    pos = b.iter_positions().next()
    pos = (5,1)
    b[pos] = board._black
    print(b)
    for adj in b.tower_adjacencies[pos]:
        b[adj] = board._black
    print(b)

def test_is_valid():
    valid_boards = [
Board('''
 1  
    
'''),
Board('''
 1. 
    
'''),
Board('''
 0. 
 .  
'''),
Board('''
    
  X 
'''),
Board('''
 ...
 .X.
'''),
Board('''
   ..X..
  .X....X
  .X..X..
   ..X..
'''),
Board('''
   .X...
  ..X..X.
  ...X.X.
   X....
'''),
Board('''
   .X...
  ..X..X.
  X.. .X.
   ..X..
'''),
Board('''
   ..X..
  .X... .
  .X..X..
   ..X..
'''),
]   
    invalid_boards = [
Board('''
 1X 
 X  
'''),
Board('''
 XX.
 .X.
'''),
Board('''
   .   .
  . .2. .
  .     .
   .   .
'''),
Board('''
   ..X..
  .X.....
  .X..X..
   ..X..
'''),
Board('''
   ..X..
  ..X..X.
  .X...X.
   ..X..
'''),
Board('''
   .X...
  ..X..X.
  X....X.
   ..X..
'''),
]   

    print 'testing valid boards...'
    valid_passed = True
    for board in valid_boards:
        if not board.is_valid():
            print(board)
            print('invalid (FAILED)')
            valid_passed = False
    if valid_passed:
        print('valid boards PASSED')

    print 'testing invalid boards...'
    invalid_passed = True
    for board in invalid_boards:
        if board.is_valid():
            print board
            print('valid (FAILED)')
            invalid_passed = False
    if invalid_passed:
        print('invalid boards PASSED')

    return valid_passed and invalid_passed

if __name__ == '__main__':
    #print 'running...'
    #import cProfile
    #from pstats import Stats
    #stats_file = "tritower.stat"
    #cProfile.run("test_solve()", stats_file)
    #stats = Stats(stats_file)
    #stats.sort_stats('time')
    #stats.print_stats()    

    print 'pass' if test_solve() else 'fail'
    test_tower_adjacencies()
    test_is_valid()
    
    t = Board('''
                
                 
     0            
                   
        1          
            1 2  1
       2  2      
        1 1  2  
''')
    #print t.solve()
