from board import Board

class TriangleGrid(Board):
    def _in_bounds(self, x, y):
        """Determine whether a particular point is within the hexagonal boundary of the board."""
        if y < 0 or y >= self.ysize or x < 0 or x >= self.xsize:
            self.bounds_dict[(x,y)] = False
            return False # outside allocation area

        dist = 2*(self.size - 1)
        fromright = self.xsize - x - 1
        frombottom = self.ysize - y - 1

        # lines creating sides of the hex
        topleft = x + y > dist
        topright = fromright + y > dist
        bottomleft = x + frombottom > dist
        bottomright = fromright + frombottom > dist

        result = topleft and topright and bottomleft and bottomright
        return result


    def _cull_bounds(self, position_list):
        """Remove all positions that are out of bounds, and return the remainder."""
        return [(x,y) for (x,y) in position_list if (x,y) in self.positions]


    def _adjacencies(self, pos):
        """Return all in-bounds adjacencies of the given position."""

        x, y = pos

        adjacency_list = [(x-1,y), (x+1,y)] # add left and right spaces

        if (x+y)%2 == 0: # even triangle, pointing down
            adjacency_list.append((x,y-1))
        else: # odd triangle, pointing up
            adjacency_list.append((x,y+1))

        return self._cull_bounds(adjacency_list)


    def _tower_adjacencies(self, pos):
        """Return all in-bounds corner-adjacencies of the given position."""

        x, y = pos

        # add 2-left, 2-right, and diagonal spaces
        adjacency_list = [(x-2,y), (x+2,y), (x-1,y-1),(x+1,y-1),(x-1,y+1),(x+1,y+1)]

        if (x+y)%2 == 0: # even triangle, pointing down
            adjacency_list.extend([(x,y+1),(x-2,y-1),(x+2,y-1)])
        else: # odd triangle, pointing up
            adjacency_list.extend([(x,y-1),(x-2,y+1),(x+2,y+1)])

        return self._cull_bounds(adjacency_list)


    def __str__(self):
        s = ''
        height = self.size*4 + 1
        n = 0
        row = 0
        slash = '/'
        iter_self = iter(self)

        while True:
            # border line
            margin = self.size*2 - min(n, height-n-1)
            border_length = self.size + min(row, self.size*2 - row)
            s += ' '*margin
            s += '*---'*border_length + '*\n'
            n += 1

            if not n < height:
                break

            row += 1

            # triangle line
            margin = self.size*2 - min(n, height-n-1)
            row_length = 2*(self.size + min(row, 2*self.size - row + 1))

            s += ' '*margin

            if row == self.size + 1: # adjust slashes after midpoint
                slash = '\\'

            i = 0
            while True:
                s += slash
                if slash == '/': slash = '\\'
                else: slash = '/'
                i += 1
                if not i < row_length:
                    break
                s += chars[iter_self.next()]
                
            s += '\n'
            n += 1

        return s[:-1]
