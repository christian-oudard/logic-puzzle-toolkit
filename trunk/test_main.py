#! /usr/bin/env python

# test new solve function #
import unittest
from constants import SET_DEBUG
from test_mines import TestMines
from test_tritower import TestTritower
from test_widetower import TestWidetower
from test_nurikabe import TestNurikabe
from test_slitherlink import TestSlitherLink
from test_masyu import TestMasyu
from test_mochikoro import TestMochikoro

if __name__ == '__main__':
#    SET_DEBUG(3)
    import sys
    sys.argv.append('-v')
    unittest.main()
