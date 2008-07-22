def pairwise(iterable, loop=False):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    try:
        if loop:
            b = roll(b, 1)
        else:
            b = islice(b, 1, None)
    except StopIteration:
        pass
    return izip(a, b)

def triplewise(iterable, loop=False):
    """s -> (s0,s1,s2), (s1,s2,s3), ..."""
    a, b, c = tee(iterable, 3)
    try:
        if loop:
            b = roll(b, 1)
            c = roll(c, 2)
        else:
            b = islice(b, 1, None)
            c = islice(c, 2, None)
    except StopIteration:
        pass
    return izip(a, b, c)

def roll(iterable, num=1):
    """Rolls num elements from the beginning to the end of the iterable."""
    buffer = []
    for i in range(num):
        buffer.append(iterable.next())
    return chain(iterable, buffer)

# from raymond hettinger
from itertools import izip, chain, repeat
def izip_longest(*args, **kwds):
    ''' Alternate version of izip() that fills-in missing values rather than truncating
    to the length of the shortest iterable.  The fillvalue is specified as a keyword
    argument (defaulting to None if not specified).

    >>> list(izip_longest('a', 'def', 'ghi'))
    [('a', 'd', 'g'), (None, 'e', 'h'), (None, 'f', 'i')]
    >>> list(izip_longest('abc', 'def', 'ghi'))
    [('a', 'd', 'g'), ('b', 'e', 'h'), ('c', 'f', 'i')]
    >>> list(izip_longest('a', 'def', 'gh'))
    [('a', 'd', 'g'), (None, 'e', 'h'), (None, 'f', None)]
    '''
    fillvalue = kwds.get('fillvalue')
    def sentinel(counter=[fillvalue]*(len(args)-1)):
        yield counter.pop()     # raises IndexError when count hits zero
    iters = [chain(it, sentinel(), repeat(fillvalue)) for it in args]
    try:
        for tup in izip(*iters):
            yield tup
    except IndexError:
        pass
