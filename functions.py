from numbers import *

def srange(start, stop, step=sint('1')):
    start, stop, step = sint(start), sint(stop), sint(step)
    i = sint(start)
    while i != stop:
        yield i
        i += step

def sfact(k):
    k = sint(k)
    n = sint('1')
    for i in srange('1',k+'1'):
        n *= i
    return n

def ssum(itr):
    k = sint('0')
    for i in itr:
        k += i
    return k

def sabs(k):
    return sint(k,sign=False)