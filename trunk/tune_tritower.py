from __future__ import division

from constants import SET_DEBUG
from tritower import Tritower
from widetower import Widetower

def main():
    #print run()
    #vals = [.02, .05, .08, .1, .15, .2]
    #vals = [0, 0.1, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0]
    vals = [1.8 + e for e in (-1, -.5, -.2, -.1, 0, .1, .2, .5, 1)]
    #vals = [p / 10 for p in range(12)]
    #vals = range(4)
    stats = []
    for v in vals:
        stats.append(run(v))
    show_stats(stats)

def run(*args):
    tunables = args
    if tunables:
        (
#            Widetower.conclusion_adjacent_value,
#            Widetower.conclusion_corner_adjacent_value,
#            Widetower.given_adjacent_value,
#            Widetower.given_corner_adjacent_value,
            Widetower.known_adjacent_value,
#            Widetower.known_corner_adjacent_value,
        ) = tunables
    print
    print tunables
    puzzles = create_puzzles()
    sum = 0
    for puz in puzzles:
        puz.solve(1, True)
        sum += puz.is_valid_count
        print puz.is_valid_count
        
    return (tunables, sum)

def show_stats(stats):
    stats.sort(key=lambda x: x[1])
    print
    print 'sums'
    for val, sum in stats:
        print '%s: %i' % (val, sum)

def create_puzzles():
    return [
        Widetower('''
                  *--2--
                  -----4-  
                  -2---3-  
                  *--3-2  
                  '''),
        Widetower('''
                  *2----   
                  ---4--1  
                  --5-4--  
                  *-2---   
                  '''),
        Widetower('''
                  *2----   
                  -----4-  
                  --4--3-  
                  *---3-   
                  '''),
        Widetower('''
                  *-1---
                  -------
                  ----4--
                  *--2--
                  '''),
        Widetower('''
                  ***-------
                  **2----45--
                  *----------1 
                  *-2--------- 
                  **--3--3--- 
                  ***-2----3
                  '''),
    ]

if __name__ == '__main__':
    main()
