from __future__ import division

from constants import SET_DEBUG
from slitherlink import SlitherLink


def main():
    #print run()
    #vals = [1.0, 1.1, 1.3, 1.5, 2.0]
    vals = [p / 10 for p in range(40)]
    #vals = range(5)
    stats = []
    for v in vals:
        stats.append(run(v))
    show_stats(stats)

def run(*args):
    tunables = args
    if tunables:
        (
            #SlitherLink.conclusion_distance_values[4],
            #SlitherLink.given_adjacent_values[0],
            SlitherLink.known_adjacent_value,
            #SlitherLink.conclusion_adjacent_value,
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
        SlitherLink('''
                    --31
                    1---
                    3--3
                    12--
                    '''),
        SlitherLink('''
                    -3--
                    -0-2
                    1-3-
                    -1-1
                    '''),
        SlitherLink('''
                    1-211
                    --2--
                    --02-
                    -----
                    112-1
                    '''),
        SlitherLink('''
                    ----0-
                    33--1-
                    --12--
                    --20--
                    -1--11
                    -2----
                    '''),
        SlitherLink('''
                    ---02--
                    ----3-3
                    -312--2
                    ----3-2
                    2-----3
                    3----3-
                    -320---
                    '''),
    ]

if __name__ == '__main__':
    main()
