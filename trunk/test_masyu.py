import unittest
from masyu import Masyu

class TestMasyu(unittest.TestCase):
    straight_junctions = [
        Masyu('''
              + + +
                |  
              +.+.+
                |  
              + + +
              '''),
        Masyu('''
              + + +
                .  
              +-+-+
                .  
              + + +
              '''),
        Masyu('''
              + + +
                |  
              + + +
                |  
              + + +
              '''),
        Masyu('''
              + + +
                   
              +-+-+
                   
              + + +
              '''),
        Masyu('''
              + + +
                .  
              +-+ +
                .  
              + + +
              '''),
        Masyu('''
              + + +
                   
              +.+.+
                   
              + + +
              '''),
        Masyu('''
              + + +
                .  
              + + +
              '''),
    ]
    bent_junctions = [
        Masyu('''
              + + +
                .  
              +-+.+
                |  
              + + +
              '''),
        Masyu('''
              + + +
                |  
              +-+ +
                   
              + + +
              '''),
        Masyu('''
              + + +
                .  
              + + +
                |  
              + + +
              '''),
        Masyu('''
              + + +
                |  
              + + +
                .  
              + + +
              '''),
        Masyu('''
              + + +
                   
              +-+.+
                   
              + + +
              '''),
        Masyu('''
              + + +
                   
              +.+-+
                   
              + + +
              '''),
        Masyu('''
              + + +
                   
              +.+ +
                .  
              + + +
              '''),
        Masyu('''
              + + +
                   
              +.+ +
              '''),
        Masyu('''
              + +
                 
              + +
              '''),
    ]
    unknown_junctions = [
        Masyu('''
              + + +
                   
              + + +
                   
              + + +
              '''),
        Masyu('''
              + + +
                   
              +-+ +
                   
              + + +
              '''),
        Masyu('''
              + + +
                .  
              + + +
                   
              + + +
              '''),
        Masyu('''
              + + +
                   
              +-+ +
                .  
              + + +
              '''),
    ]

    def test_is_bent_true(self):
        for junction in self.bent_junctions:
            self.assertTrue(junction.is_bent((1, 1)), 'this junction should be bent:\n%r' % junction)
     
    def test_is_bent_false(self):
        for junction in self.straight_junctions + self.unknown_junctions:
            self.assertFalse(junction.is_bent((1, 1)), 'this junction should not be bent:\n%r' % junction)
     
    def test_is_straight_true(self):
        for junction in self.straight_junctions:
            self.assertTrue(junction.is_straight((1, 1)), 'this junction should be straight:\n%r' % junction)
     
    def test_is_straight_false(self):
        for junction in self.bent_junctions + self.unknown_junctions:
            self.assertFalse(junction.is_straight((1, 1)), 'this junction should not be straight:\n%r' % junction)
     
    def test_valid_junction_givens_fail(self):
        invalid_boards = [
            Masyu('''
                  + + + + +

                  + + + + +

                  + +.@.+ +

                  + + + + +

                  + + + + +
                  '''),
            Masyu('''
                  + + + + +

                  + + + + +

                  + + @-+ +
                        | 
                  + + + + +

                  + + + + +
                  '''),
            Masyu('''
                  + + + + +

                  + + + + +
                      .
                  + +.0 + +
                          
                  + + + + +

                  + + + + +
                  '''),
            Masyu('''
                  + + + + +

                  + + + + +

                  +-+-0-+-+
                          
                  + + + + +

                  + + + + +
                  '''),
            Masyu('''
                  + + + + +

                  + + + + +
                      .
                  + +.0.+ +
                      .    
                  + + + + +

                  + + + + +
                  '''),
            Masyu('''
                  + + + + +

                  + + + + +
                      .
                  + +.@.+ +
                      .
                  + + + + +

                  + + + + +
                  '''),
        ]
        for ib in invalid_boards:
            self.assertFalse(ib.valid_junction_givens(), 'board tested valid:\n%r' % ib)

    def test_valid_junction_givens_pass(self):
        valid_boards = [
            Masyu('''
                  + + + + +

                  + + + + +

                  + + 0 + +
                          
                  + + + + +

                  + + + + +
                  '''),
            Masyu('''
                  + + + + +

                  + + + + +

                  + + @ + +
                          
                  + + + + +

                  + + + + +
                  '''),
            Masyu('''
                  + + + + +

                  + + + + +

                  +-+-0-+ +
                          
                  + + + + +

                  + + + + +
                  '''),
            Masyu('''
                  + + + + +
                      |
                  + + + + +
                      |
                  + + 0 + +
                          
                  + + + + +

                  + + + + +
                  '''),
        ]
        for vb in valid_boards:
            self.assertTrue(vb.valid_junction_givens(), 'board tested invalid:\n%r' % vb)

    def test_solve(self):
        test_boards = [
            (
                Masyu('''
                      --@-@--
                      -----0-
                      0------
                      -000---
                      -----@0
                      @------
                      ---00--
                      '''),
                Masyu('''
                      +.+.@-+-@.+-+
                      . . | . | | |
                      +-+.+.+.+.0.+
                      | | | . | | |
                      0.+.+.+-+.+.+
                      | | | | . | |
                      +.0.0.0.+.+.+
                      | | | | . | |
                      +.+-+.+-+-@.0
                      | . . . . . |
                      @-+-+.+.+.+-+
                      . . | . . | .
                      +.+.+-0-0-+.+
                      ''')
            )
        ]
        for unsolved_board, solved_board in test_boards:
            unsolved_board.solve()
            self.assertEqual(unsolved_board, solved_board)
