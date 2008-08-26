from constants import *
from nurikabe import Nurikabe

class Mochikoro(Nurikabe):
    def is_valid(self, position=None, color=None):
        return all((
            self.valid_no_black_2by2(position, color),
            self.valid_white_rectangles(),
            self.valid_white_groups(position, color),
            self.valid_white_corner_connected(),
        ))

    def valid_white_rectangles(self):
        for pos in self.black_positions.union(self.white_positions):
            x, y = pos
            square = [(x, y),
                      (x+1, y),
                      (x, y+1),
                      (x+1, y+1)]
            try:
                num_white = 0
                for s in square:
                    color = self[s]
                    if color == UNKNOWN:
                        break
                    if color == WHITE:
                        num_white += 1
                if num_white == 3:
                    return False
            except KeyError:
                continue # square at edge, ignore it
        return True

    def valid_white_corner_connected(self):
        pass



