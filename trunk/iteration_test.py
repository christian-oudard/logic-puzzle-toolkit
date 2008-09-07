from itertools import izip
positions = [1, 2]
MAX_DEPTH = 3
class I(object):
    def solve(self):
        t = self.solution_thread(1, ['root'])
        for r in t:
            pass

    def solution_thread(self, depth, call_stack):
        print '-'.join(call_stack)
        while True:
            for result in self.conclusion_thread(depth, call_stack+['ct']):
                if result == 'fail':
                    return
                yield result

    def conclusion_thread(self, depth, call_stack):
        print '-'.join(call_stack)
        threads = []
        for pos in positions:
            threads.append(self.assumption_thread(pos, depth, call_stack+['at']))
        while threads:
            finished_threads = []
            for t in threads:
                try:
                    result = t.next()
                except StopIteration:
                    finished_threads.append(t)
                #STUB, check result
            for ft in finished_threads:
                threads.remove(ft)
            yield
        yield 'fail'

    def assumption_thread(self, position, depth, call_stack):
        print '-'.join(call_stack)
        yield
        if depth > MAX_DEPTH:
            print 'limit'
            return
        stb = self.solution_thread(depth+1, call_stack + ['st'+str(position)+'B'])
        stw = self.solution_thread(depth+1, call_stack + ['st'+str(position)+'W'])
        for rb in stb:
            pass
        for rw in stw:
            pass
#       for rb, rw in izip(stb, stw):
#           yield 

I().solve()
