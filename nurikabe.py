from constants import *
import valid
from utility import mdist
from squaregrid import SquareGrid

class Nurikabe(SquareGrid):
    def valid_no_black_2by2(self, position=None, color=None):
        if color == WHITE:
            return True
        candidates = self.black_positions
        if position:
            x, y = position
            square = [position,
                      (x-1, y),
                      (x, y-1),
                      (x-1, y-1)]
            candidates = candidates.intersection(square)
        for pos in candidates:
            x, y = pos
            square = [pos,
                      (x+1, y),
                      (x, y+1),
                      (x+1, y+1)]
            try:
                if all(self.is_black(s) for s in square):
                    return False
            except KeyError:
                continue # square at edge, ignore it
        return True
    
    def valid_white_groups(self, position=None, color=None):
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

        # find orphaned groups
        def search_white_orphan(pos):
            orphan_marks[pos] = 'visited'
            for adj in self.adjacencies[pos]:
                if self.is_black(adj):
                    continue
                if self.is_white(adj) and marks[adj] == 'visited':
                    return WHITE
                if orphan_marks[adj] == WHITE:
                    return WHITE
                if orphan_marks[adj] == 'unvisited': # white or unknown, and unvisited
                    if search_white_orphan(adj) == WHITE:
                        orphan_marks[adj] = WHITE
                        orphan_marks[pos] = WHITE
                        return WHITE
            return BLACK

        orphan_marks = {}
        for pos in marks:
            if marks[pos] == 'unvisited':
                orphan_marks[pos] = 'unvisited'
        for pos in self.unknown_positions:
            orphan_marks[pos] = 'unvisited'

        for pos in orphan_marks:
            if orphan_marks[pos] == 'unvisited' and self.is_white(pos):
                if search_white_orphan(pos) == BLACK:
                    return False # orphan group can't connect to a given number

        return True

    def valid_white_reachable(self, position=None, color=None):
        if color == BLACK:
            return True
        if color == WHITE:
            candidates = [position]
        else:
            candidates = self.white_positions.difference(self.given_positions)
        for pos_white in candidates:
            for pos_given in self.given_positions:
                number = self[pos_given]
                if mdist(pos_given, pos_white) < number:
                    break # this candidate has a given close enough
            else:
                return False # no numbers close enough
        return True

    validity_checks = (
        valid_no_black_2by2,
        valid_white_groups,
        valid.black_connected,
        valid_white_reachable,
    )

    conclusion_adjacent_value = 3
    conclusion_corner_adjacent_value = 4.5
    conclusion_distance_values = {
        2: 4,
        3: .5,
    }
    known_adjacent_value = 1
    def priority(self, position):
        score = 0
        if self.last_conclusion is not None:
            if self.last_conclusion in self.adjacencies[position]:
                score += self.conclusion_adjacent_value
            elif self.last_conclusion in self.corner_adjacencies[position]:
                score += self.conclusion_corner_adjacent_value
            else:
                dist = mdist(self.last_conclusion, position)
                if dist in self.conclusion_distance_values:
                    score += self.conclusion_distance_values[dist]
        for adj in self.adjacencies[position]:
            if not self.is_unknown(adj):
                score += self.known_adjacent_value
        return score
