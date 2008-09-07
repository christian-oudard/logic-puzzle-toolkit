#! /usr/bin/env python

import cProfile
from pstats import Stats

from constants import *
from nurikabe import Nurikabe
from tritower import Tritower
from mines import Mines

def solve_tiny():
    puzzle = Mines('''
        2---
        --1-
        -2--
        ---1
    ''')
    puzzle.solve()

def solve_small():
    puzzle = Mines('''
        --2-3-
        2-----
        --24-3
        1-34--
        -----3
        -3-3--
    ''')
    puzzle.solve()

def solve_medium_nurikabe():
    puzzle = Nurikabe('''
        2--------2
        ------2---
        -2--7-----
        ----------
        ------3-3-
        --2----3--
        2--4------
        ----------
        -1----2-4-
    ''')
    puzzle.solve(3)

def solve_medium_tritower():
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
2----1-------1------2---
--------2---3----1------
-----1-------1--3------6
-1------5---------------
------4------1--------3-
---------------7-7-3----
-----2------------------
--9---------------------
-7-1---4-----2----1-----
----------5---------1---
---4-4-------------2----
----8-----------------7-
------1------5----b----5
--------6-2-----5-------
''')
    puzzle.solve()

def solve_large_ip():
    puzzle = Nurikabe('''
2XXXX1XXXXXXX1XXXXX-2---
.X..XXX.2X..3XX.X1X-X---
XXX.X1XXX-XXX1X.3X-----6
X1X.XX--5--.-XXXX-----X-
.XX.X.4-----X1X.X--X-X3X
.X..XX-------X-7X7X3X..X
.X.X.2X----------.X.XXXX
.X9XXXX-----------X.X..X
.7X1X.X4-----2X--X1XXX.X
.XXXX.X---5----...XX1X.X
XX.4X4.X------XXX.X2XX.X
X..X8XXX.------.X.X.X.7X
XXXX.X1X.X-X-5X.X.bXXXX5
......XX6X2-XX-.5XXX....
''')
    puzzle.solve()

def solve_huge():
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
    puzzle.limit = 1000
    puzzle.solve()

def solve_huge_ip():
    puzzle = Nurikabe('''
                      XX---------------XXXXXXXXXXX--------
                      --2X3X7---Xb----X2.X1X....X1X-------
                      -X--------4X--.-XXX1XXXXX.7X--9-----
                      ---5---X------XX..8XX..3X.XX--XX4---
                      ---X--X1X----X1X..X..XXXXX1X-X2.XX--
                      X-X1XX1X--X-X1X..XX3X3X4..X--3XXX1X-
                      X--X2-X--X1X6XXX.X3XX..X.XX------X--
                      ---------XX-.X1XXX..XXXXX.X----.----
                      --X----.X1X.-XX...XXX...X3Xa--X8X---
                      -3X4-XX8-X--X1XX4XX1X.XXX.X..X1X1X--
                      XX6XX.2X-----XX1XX1XX5X.XXX.XXXXX--7
                      X...XXXX4.---X1XX1XX1X..X1X.X1X1X---
                      X.XXX.4.XXX-.XX..XX.XXX4XX1XXX4XX---
                      X.X1X.XXX1X--X1X.....X6X1XX3X...X---
                      XX1XXX3..XX6.XXXX9XXXX.XX1X..XXX1X--
                      X.X...XXXX1XXX..4XX1X...XX4XX-4-X--5
                      X2XX..X1X.X2.XX.X2.XXX.XX...X..-----
                      XXX1X6XX..XXX1XXXXXX..XX1XXXX-XXX---
                      X.XXXX1X.XX1XXX...X1X4.XXX3..X.X1XX-
                      X.5X.XX.6X1X3.XX4XXXXXX1X6XXXX..XX2X
                      X.X4..XXX.XX.X.XX1X...XX...X.X4X1X.X
                      X.XXXXX.X2X1XX..5XXX4XX..XXX.3XXX4XX
                      XX4...X.8XXXX1X.X-.-X.XXX5X1XXX.X..X
                      X3XXXX1X.---6XXX-X4.X2X.-.-XX1X3X.XX
                      X.X..4XX--------..XXXX--X.---XX.XX3X
                      X.XX.XX.-------XX4X2.X..7XX..4XX.X.X
                      XX1XX1X--------.8X7XX--XX1XXXX1X.X.X
                      X.X2XX4---------XX..----4XX3X1XX3XXX
                      X2X.X..X5--------3X-----..X..X.2X2.X
                      XXXXX--X------------------XXXXXXXXXX
                      ''')
    puzzle.solve()

def time_main(command):
    stats_file = 'lpt.stat'
    cProfile.run('from timing_main import *; ' + command, stats_file)
    stats = Stats(stats_file)
    stats.sort_stats('cum')
    stats.print_stats()

if __name__ == '__main__':
    SET_DEBUG(1)
    #time_main('solve_huge2()')
    solve_huge_ip()
    #solve_large_ip()
