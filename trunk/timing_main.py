import cProfile
from pstats import Stats

import board
from nurikabe import Nurikabe
from tritower import Tritower

def solve_medium():
    board.solve_report = True
    puzzle = Tritower('''
           ---------
          -----------
         0------------
        ---------------
        ----1----------
         -------1-2--1
          -2--2------
           -1-1--2--
    ''')
    puzzle.solve()

def solve_big():
    #board.max_steps = 10000
    board.solve_report = True
    puzzle = Nurikabe('''
------------------------------------
--2-3-7----B-----2--1------1--------
----------4--------1------7---9-----
---5--------------8----3--------4---
-------1------1-----------1---2-----
---1--1------1-----3-3-4-----3---1--
----2-----1-6-----3-----------------
--------------1---------------------
---------1---------------3-A---8----
-3-4---8-----1--4--1----------1-1---
--6---2--------1--1--5-------------7
--------4-----1--1--1----1---1-1----
------4----------------4--1---4-----
---1-----1----1-------6-1--3--------
--1---3----6-----9-------1------1---
----------1-----4--1------4---4----5
-2-----1---2-----2------------------
---1-6-------1----------1-----------
------1----1-------1-4----3-----1---
--5-----6-1-3---4------1-6--------2-
---4-------------1------------4-1---
---------2-1----5---4--------3---4--
--4-----8----1-----------5-1--------
-3----1-----6-----4--2-------1-3----
-----4----------------------------3-
-----------------4-2----7----4------
--1--1----------8-7------1----1-----
---2--4-----------------4--3-1--3---
-2------5--------3-------------2-2--
------------------------------------
''')
    puzzle.solve()
    
def time_main():
    stats_file = 'lpt.stat'
    cProfile.run('solve_medium()', stats_file)
    stats = Stats(stats_file)
    stats.sort_stats('time')
    stats.print_stats()

if __name__ == '__main__':
    time_main()
