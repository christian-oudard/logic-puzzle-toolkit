import board
import valid
from squaregrid import SquareGrid

class Mines(SquareGrid):
    validity_checks = (
        valid.given_neighbors_corner,
    )

