from __future__ import division

from nurikabe import Nurikabe
from constants import SET_DEBUG

def main():
    run()
#    vals = [4.1, 4.3, 4.5, 4.7, 4.9]
#    vals.reverse()
#    for v in vals:
#        run(v)

def run(*args):
    tunables = args
    if tunables:
        (
            Nurikabe.conclusion_distance_values[2],
        ) = tunables
    print
    print tunables
    puzzles = create_puzzles()
    for puz in puzzles:
        puz.solve(1, True)
        print puz.is_valid_count

def create_puzzles():
    return [
        Nurikabe('''
                 -a----3--3
                 --5-------
                 ----------
                 -----5---4
                 5---4-----
                 ----------
                 ----------
                 -------3--
                 2--2----2-
                 '''),
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
                 2--------2
                 ------2---
                 -2--7-----
                 ----------
                 ------3-3-
                 --2----3--
                 2--4------
                 ----------
                 -1----2-4-
                 '''),
        Nurikabe('''
                 -----8--2-
                 -7----2---
                 ----------
                 -----2----
                 -------4--
                 --3---5---
                 3---------
                 --2-2-----
                 -------2-2
                 ----------
                 '''),
        Nurikabe('''
                 --5-----6-
                 ----------
                 -----2----
                 ----------
                 --------6-
                 2---5--4--
                 ----------
                 4----2----
                 ---------2
                 ---5-5----
                 '''),
    ]

if __name__ == '__main__':
    main()
