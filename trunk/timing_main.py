#! /usr/bin/env python

import cProfile

from pstats import Stats

from constants import *
import board
from nurikabe import Nurikabe
from tritower import Tritower
from mines import Mines

def solve_small():
    puzzle = Mines('''
        2---
        --1-
        -2--
        ---1
    ''')
    puzzle.solve()

def solve_medium():
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

def solve_large():
    puzzle = Nurikabe('''
------------------------------------
--2-3-7----b-----2--1------1--------
----------4--------1------7---9-----
---5--------------8----3--------4---
-------1------1-----------1---2-----
---1--1------1-----3-3-4-----3---1--
----2-----1-6-----3-----------------
--------------1---------------------
---------1---------------3-a---8----
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
    puzzle = Nurikabe('''
--------------------X------X--------
--2X3X7---Xb-----2-X1X----X1X-------
----------4X-----XX1X----.7X--9-----
---5---X------X--.8XX--3--X---XX4---
---X--X1X----X1X--X..X-X-X1X-X2.XX--
--X1XX1X--X-X1X---X3X3X4--X--3XXX1X-
---X2-X--X1X6XX---3XX.-----------X--
---------XX-.X1X---------------.----
--X-----X1X--XX..--X-----3Xa--X8X---
-3X4-XX8-X--X1XX4-X1X--------X1X1X--
-X6XX.2X-----XX1XX1XX5---X---XXXX--7
--.--XX-4----X1XX1XX1X-.X1X-X1X1X---
---X--4--X----X--X--X-X4XX1X-X4X----
--X1X-X-X1X--X1X-.----6X1XX3--.-X---
-X1X--3--XX6--X-X9XX---XX1X---XX1X--
--X----X-X1XX--.4XX1X----X4---4-X--5
-2-X-.X1X-X2.X--X2.X----X-----------
--X1X6XX---XX1X--XXX---X1X------X---
---X-X1X-XX1XX--..X1X4-XXX3----X1X--
--5X--X-6X1X3---4XXX--X1X6X-XX.-X-2-
--X4----X.XX---XX1X.---X-.-X.X4X1X--
--------X2X1XX--5X--4----X-X.3X-X4--
-X4---X-8X-XX1X----------5X1XX------
-3X--X1X----6X---X4--2-----XX1X3----
----.4X---------..XXX--------X----3-
--X--X---------XX4X2.X--7X--.4X-----
-X1XX1X--------.8X7XX--XX1X-XX1X.---
--X2-X4---------XX..----4X-3X1XX3X--
-2------5--------3X----------X-2X2--
--------------------------------X---
''')
    puzzle.solve()
    
def time_main():
    stats_file = 'lpt.stat'
    cProfile.run('from timing_main import *; solve_medium()', stats_file)
    stats = Stats(stats_file)
    stats.sort_stats('time')
    stats.print_stats()

if __name__ == '__main__':
    #time_main()
    SET_DEBUG(3)
    solve_small()
    #solve_medium()
    #solve_large()
