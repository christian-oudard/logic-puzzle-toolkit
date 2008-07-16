# debug
DEBUG_LEVEL = 0
def SET_DEBUG(level):
    global DEBUG_LEVEL
    DEBUG_LEVEL = level
def DEBUG1(): return DEBUG_LEVEL >= 1
def DEBUG2(): return DEBUG_LEVEL >= 2

# board space status codes
BLACK = -1
WHITE = -2
UNKNOWN = -3
OUT_OF_BOUNDS = -4
CONTRADICTION = -5
GIVENS = range(36)

# dictionaries to convert from constants to strings
CHARS = {
    BLACK: 'X',
    WHITE: '.',
    UNKNOWN: '-',
    OUT_OF_BOUNDS: '*',
    CONTRADICTION: '!',
    }
for g in range(10):
    CHARS[g] = str(g) # digits 0 through 9
for g in range(26):
    CHARS[g + 10] = chr(ord('a') + g) # a = 10 through z = 35
RCHARS = {}
for key, value in CHARS.iteritems():
    RCHARS[value] = key

# convenience function to check success
def is_success(result):
    return result != UNKNOWN and result != CONTRADICTION and result is not None

