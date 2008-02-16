import cProfile
from pstats import Stats

from mines import Mines

def test_solve():
    puzzle = Mines('''
    --2-3-
    2-----
    --24-3
    1-34--
    -----3
    -3-3--''')
    puzzle.solve()
    
def time_main():
    stats_file = 'lpt.stat'
    cProfile.run('test_solve()', stats_file)
    stats = Stats(stats_file)
    stats.sort_stats('time')
    stats.print_stats()

if __name__ == '__main__':
    time_main()