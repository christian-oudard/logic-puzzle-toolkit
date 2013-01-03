# debug
DEBUG_LEVEL = 0
def SET_DEBUG(level):
    global DEBUG_LEVEL
    DEBUG_LEVEL = level
def DEBUG(level): return DEBUG_LEVEL >= level

# board space status codes
BLACK = -1
WHITE = -2
UNKNOWN = -3
CONTRADICTION = -4
GIVENS = range(36)

# convenience function to check success
def is_success(result):
    return (
        result != UNKNOWN and
        result != CONTRADICTION and
        result is not False and
        result is not True and
        result is not None)

