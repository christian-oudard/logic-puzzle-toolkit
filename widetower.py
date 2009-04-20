import valid
from tritower import Tritower

class Widetower(Tritower):
    validity_checks = (
        valid.black_separate,
        valid.given_neighbors_corner,
        Tritower.valid_white_triangles,
        valid.white_edge_reachable,
        valid.black_connected_corner,
    )

    # uses tritower's priority function, but changes some tuning parameters
    conclusion_adjacent_value = 1.3 
    conclusion_corner_adjacent_value = 2
    given_adjacent_value = 1.2 
    given_corner_adjacent_value = 0.1
    known_adjacent_value = 1.8 
    known_corner_adjacent_value = 0.1
