from constants import *
from squaregrid import SquareGrid

group_count = 0 # workaround until nonlocal keyword is available

class Nurikabe(SquareGrid):
    def is_valid(self, position=None, color=None):
        return all((
            self.valid_white_groups(position, color),
            self.valid_black_connected(position, color),
            self.valid_no_black_2by2(position, color),
        ))
    
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
        if position:
            next_to_white = any(self.is_white(adj) for adj in self.adjacencies[position])
            if color == BLACK and not next_to_white:
                return True
            only_next_to_unknown = all(self.is_unknown(adj) for adj in self.adjacencies[position])
            if color == WHITE and only_next_to_unknown:
                return True

        global group_count
        marks = {}
        for pos in self.white_positions:
            marks[pos] = 'unvisited' # initialize marks

        def search_white(pos):
            global group_count
            group_count += 1
            if marks[pos] == 'visited':
                return CONTRADICTION # found given numbers connected to each other
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
                
        # mark every numbered group visited, and check that the number is correct
        for pos in self.given_positions:
            number = self[pos]
            group_count = 0
            search_result = search_white(pos)
            if search_result == CONTRADICTION:
                return False
            if search_result == BLACK and group_count != number:
                return False
            elif search_result == UNKNOWN:
                if group_count > number:
                    return False

        # find orphan groups
        for pos in marks:
            if marks[pos] == 'unvisited':
                group_count = 0
                bordered_by = search_white(pos) 
                if bordered_by == BLACK:
                    return False # orphan group can't connect to a given number

        return True
    
    def valid_black_connected(self, position=None, color=None):
        if position:
            next_to_black = any(self.is_black(adj) for adj in self.adjacencies[position])
            if color == BLACK and next_to_black:
                return True
            elif color == WHITE and not next_to_black:
                return True
        def search_black(pos): # just mark everything in the group 'visited'
            marks[pos] = 'visited'
            adjs = self.adjacencies[pos]
            for adj in adjs:
                if adj in marks and marks[adj] == 'unvisited':
                    search_black(adj)
        marks = {}
        for pos in self.black_positions.union(self.unknown_positions):
            marks[pos] = 'unvisited' # init marks
        group_count = 0
        for pos in self.black_positions: # for every unvisited tower
            if marks[pos] == 'unvisited': # don't start a group with an unknown space
                group_count += 1
                if group_count >= 2:
                    return False
                search_black(pos)
        return True

