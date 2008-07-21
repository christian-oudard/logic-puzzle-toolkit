#! /usr/bin/env python

# test new solve function #
import unittest
from test_mines import TestMines
from test_tritower import TestTritower
from test_widetower import TestWidetower
from test_nurikabe import TestNurikabe

if __name__ == '__main__':
    import sys
    sys.argv.append('-v')
    unittest.main()

