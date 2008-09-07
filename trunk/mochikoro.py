from constants import *
import valid
from nurikabe import Nurikabe

class Mochikoro(Nurikabe):
    def valid_white_rectangles(self, position=None, color=None):
        for pos in self.black_positions.union(self.white_positions):
            x, y = pos
            square = [(x, y),
                      (x+1, y),
                      (x, y+1),
                      (x+1, y+1)]
            try:
                num_black = 0
                num_white = 0
                for s in square:
                    if self.is_black(s):
                        num_black += 1
                    elif self.is_white(s):
                        num_white += 1
                    if num_black == 1 and num_white == 3 :
                        return False
            except KeyError:
                continue # square at edge, ignore it
        return True

    def valid_givens(self, position=None, color=None):
        if color == BLACK:
            if not any(self.is_white(adj) for adj in self.adjacencies[position]):
                return True
        if color == WHITE:
            if all(self.is_unknown(adj) for adj in self.adjacencies[position]):
                return True

        marks = {}
        for pos in self.white_positions:
            marks[pos] = 'unvisited' # initialize marks

        def search_white(pos):
            if marks[pos] == 'visited':
                return CONTRADICTION # found given numbers connected to each other
            Nurikabe.group_size += 1
            marks[pos] = 'visited'
            adjs = self.adjacencies[pos]
            results = []
            for adj in adjs:
                if self.is_black(adj):
                    results.append(BLACK)
                elif self.is_unknown(adj):
                    results.append(UNKNOWN)
                elif marks[adj] == 'unvisited': # white, and unvisited
                    results.append(search_white(adj))
            if all(r == BLACK for r in results): # bordered by black
                return BLACK
            else: # reached an unknown
                return UNKNOWN
                
        for pos in self.given_positions:
            number = self[pos]
            Nurikabe.group_size = 0
            search_result = search_white(pos)
            if search_result == CONTRADICTION:
                return False
            if search_result == BLACK and Nurikabe.group_size != number:
                return False
            elif search_result == UNKNOWN:
                if Nurikabe.group_size > number:
                    return False
        return True

    validity_checks = (
        Nurikabe.valid_no_black_2by2,
        valid_white_rectangles,
        valid.white_connected_corner,
        valid_givens,
    )
