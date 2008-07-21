import board
from board import *
from squaregrid import SquareGrid

group_count = 0 # workaround until nonlocal keyword is available

class Nurikabe(SquareGrid):
    def _is_valid(self):
        return all((
            self.valid_white_groups(),
            self.valid_black_connected(),
            self.valid_no_black_2by2(),
        ))
    
    def valid_no_black_2by2(self):
        for pos in self.black_positions:
            x, y = pos
            square = [pos,
                      (x+1, y),
                      (x, y+1),
                      (x+1, y+1)]
            if all(s in self.black_positions for s in square):
                return False
        return True
    
    def valid_white_groups(self):
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
        for pos in self.positions:
            number = self[pos]
            if number not in GIVENS:
                continue
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
                if search_white(pos) == BLACK:
                    return False # orphan group can't connect to a given number

        return True
    
    def valid_black_connected(self):
        marks = {}
        for pos in self.black_positions.union(self.unknown_positions):
            marks[pos] = 'unvisited' # init marks

        def search_black(pos): # just mark everything in the group 'visited'
            marks[pos] = 'visited'
            adjs = self.adjacencies[pos]
            for adj in adjs:
                if adj in marks and marks[adj] == 'unvisited':
                    search_black(adj)

        group_count = 0
        for pos in self.black_positions: # for every unvisited tower
            if marks[pos] == 'unvisited': # don't start a group with an unknown space
                group_count += 1
                if group_count >= 2:
                    return False
                search_black(pos)

        return True

