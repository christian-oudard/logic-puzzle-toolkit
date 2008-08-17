import unittest
from slitherlink import SlitherLink

class TestSlitherLink(unittest.TestCase):
    def test_valid_givens_pass(self):
        valid_boards = [
            SlitherLink('''
                        + +
                          
                        + +
                        '''),
            SlitherLink('''
                        0
                        '''),
            SlitherLink('''
                        01234
                        '''),
            SlitherLink('''
                        1-
                        '''),
            SlitherLink('''
                        + + +
                         1|
                        + + +
                        '''),
            SlitherLink('''
                        +-+ +
                         1  
                        + + +
                        '''),
            SlitherLink('''
                        +.+ +
                        .1. 
                        + + +
                        '''),
            SlitherLink('''
                        + + +
                         2| 
                        +-+ +

                        + + +
                        '''),
            SlitherLink('''
                        + +.+
                         2|2.
                        + +-+
                          .2
                        + +-+
                        '''),
        ]   
        for vb in valid_boards:
            self.assertTrue(vb.valid_givens(), 'board tested invalid:\n' + repr(vb))

    def test_valid_givens_fail(self):
        invalid_boards = [
            SlitherLink('''
                        +-+
                         0
                        + +
                        '''),
            SlitherLink('''
                        + +
                         4.
                        + +
                        '''),
            SlitherLink('''
                        + +
                         5
                        + +
                        '''),
            SlitherLink('''
                        + + +
                        .3.3
                        + + +
                        '''),
        ]   
        for ib in invalid_boards:
            self.assertFalse(ib.valid_givens(), 'board tested valid:\n' + repr(ib))

    def test_valid_junction_pass(self):
        valid_boards = [
            SlitherLink('''
                        +-+
                          |
                        + +
                        '''),
            SlitherLink('''
                        +-+-+
                           
                        + + +
                        '''),
            SlitherLink('''
                        +-+-+
                          .
                        + + +
                        '''),
            SlitherLink('''
                        + +.+
                          .
                        + + +
                        '''),
            SlitherLink('''
                        +.+.+
                          .
                        + + +
                        '''),
            SlitherLink('''
                        +-+ +
                          .
                        + + +
                        '''),
        ]   
        for vb in valid_boards:
            self.assertTrue(vb.valid_junction(), 'board tested invalid:\n' + repr(vb))
 
    def test_valid_junction_fail(self):
        invalid_boards = [
            SlitherLink('''
                        +.+
                          |
                        + +
                        '''),
            SlitherLink('''
                        +-+-+
                          |
                        + + +
                        '''),
            SlitherLink('''
                        +-+.+
                          .
                        + + +
                        '''),
        ]   
        for ib in invalid_boards:
            self.assertFalse(ib.valid_junction(), 'board tested valid:\n' + repr(ib))

    def test_valid_connected_fail(self):
        invalid_boards = [
            SlitherLink('''
                        +-+.+-+
                        | | | |
                        +-+.+-+
                        '''),
        ]   
        for ib in invalid_boards:
            self.assertFalse(ib.valid_connected(), 'board tested valid:\n' + repr(ib))

    def test_solve(self):
        test_boards = [
            (
                SlitherLink('''
                            -3--
                            -0-2
                            1-3-
                            -1-1
                            '''),
                SlitherLink('''
                            +.+-+.+-+
                            . |3| | |
                            +-+.+-+.+
                            | .0. .2|
                            +.+.+-+-+
                            |1. |3. .
                            +.+.+-+.+
                            | .1. |1.
                            +-+-+-+.+
                            ''')
            ),
            (
                SlitherLink('''
                            1-211
                            --2--
                            --02-
                            -----
                            112-1
                            '''),
                SlitherLink('''
                            +.+-+-+.+.+
                            .1| .2|1.1.
                            +.+-+.+.+-+
                            . . |2| | |
                            +-+-+.+-+.+
                            | . .0.2. |
                            +.+-+.+-+-+
                            | | | | . .
                            +-+.+.+-+.+
                            .1.1|2. |1.
                            +.+.+-+-+.+
                            ''')
            ),
        ]
        for unsolved_board, solved_board in test_boards:
            unsolved_board.solve()
            self.assertEqual(unsolved_board, solved_board)


