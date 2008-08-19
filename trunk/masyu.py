from constants import BLACK, WHITE, UNKNOWN
from linegrid import LineGrid
from slitherlink import SlitherLink

class Masyu(SlitherLink):
    def is_valid(self, position=None, color=None):
        return all((
            self.valid_junction(position, color),
            self.valid_junction_givens(),
            self.valid_connected(position, color),
        ))

    BENT = '@'
    STRAIGHT = '0'
    def valid_junction_givens(self):
        for jpos, type in self.junction_givens.items():
            if type == Masyu.BENT:
                if self.is_straight(jpos):
                    return False
                if any(self.is_bent(con) for con in self.connected_junctions(jpos)):
                    return False
            elif type == Masyu.STRAIGHT:
                if self.is_bent(jpos):
                    return False
                cjs = self.connected_junctions(jpos)
                if len(cjs) == 2 and all(self.is_straight(con) for con in cjs):
                    return False
        return True

    def connected_junctions(self, jpos):
        jx, jy = jpos
        x = jx * 2
        y = jy * 2
        adjacent_junctions = [(jx-1, jy),
                              (jx+1, jy),
                              (jx, jy-1),
                              (jx, jy+1)]
        adjacent_lines = [(x-1, y),
                          (x+1, y),
                          (x, y-1),
                          (x, y+1)]
        connected_junctions = []
        for jpos, pos in zip(adjacent_junctions, adjacent_lines):
            if pos in self.positions and self.is_black(pos):
                connected_junctions.append(jpos)
        return connected_junctions

    def is_bent(self, jpos):
        return self.bendiness(jpos) == Masyu.BENT

    def is_straight(self, jpos):
        return self.bendiness(jpos) == Masyu.STRAIGHT

    def bendiness(self, jpos):
        left, right, up, down = self.segment_colors(jpos)
        opposite_sides = [(left, right),
                          (up, down)]
        touching_sides = [(up, right),
                          (right, down),
                          (down, left),
                          (left, up)]
        for a, b in opposite_sides:
            if (a == WHITE and b == WHITE or
                a == BLACK and b == BLACK):
                return Masyu.STRAIGHT
            elif (a == WHITE and b == BLACK or
                  a == BLACK and b == WHITE):
                return Masyu.BENT
        for a, b in touching_sides:
            if (a == WHITE and b == WHITE or
                a == BLACK and b == BLACK):
                return Masyu.BENT

    def segment_colors(self, junction_position):
        jx, jy = junction_position
        x = jx * 2
        y = jy * 2
        adjacent_positions = [(x-1, y),
                              (x+1, y),
                              (x, y-1),
                              (x, y+1)]
        segment_colors = []
        for pos in adjacent_positions:
            try:
                color = self[pos]
            except KeyError:
                color = WHITE
            segment_colors.append(color)
        return segment_colors

    def translate_data_compact(self, data_dict):
        self.x_size = self.x_size - 1
        self.y_size = self.y_size - 1
        for pos, value in data_dict.items():
            c = data_dict.get(pos)
            if c == Masyu.BENT:
                self.junction_givens[pos] = Masyu.BENT
            elif c == Masyu.STRAIGHT:
                self.junction_givens[pos] = Masyu.STRAIGHT
                for x, y in self.iter_checker():
                    self.data[(x, y)] = UNKNOWN
