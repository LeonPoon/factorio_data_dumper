

import contextlib
import lupa
from lupa import LuaRuntime


class Lua(object):

    def __init__(self, setup):
        self.runtime = LuaRuntime()
        self.runtime.eval('function(pow) math.pow = pow end')(pow)
        setup(self.runtime)

    def evaluate(self, evaluatable):
        with self.add_searchpaths(evaluatable.get_lua_searches()):
            for m in evaluatable.get_lua_modules():
                self.runtime.eval('require("%s")' % m)
        return self

    @contextlib.contextmanager
    def add_searchpaths(self, ps):
        p, ps = (ps[0], ps[1:]) if ps else (None, ps)
        if p:
            self.set_searchpath('%s/?.lua;%s' % (p, self.runtime.eval('package.path')))
        if ps:
            with self.add_searchpaths(ps):
                yield
        else:
            yield

    def set_searchpath(self, p):
        return self.runtime.eval('function(p) package.path = p end')(p)

    def dump_global(self, v):
        return Dumper().dump(self.runtime.eval(v))


class Dumper(object):
    def __init__(self, level=0):
        self.level = level

    def dump(self, d):
        t = (lupa.lua_type(d))
        return (self.dump_table if t == 'table'
                else getattr(self, 'dump_%s' % t))(d)

    def dump_table(self, d):
        keys = tuple(d.keys())
        if tuple(set(map(type, keys))) == (int,):
            if max(keys) == len(keys) and min(keys) == 1 and len(set(keys)) == len(keys):
                return [Dumper(self.level + 1).dump(d[k]) for k in keys]
        return dict((k, Dumper(self.level + 1).dump(d[k])) for k in keys)

    def dump_function(self, d):
        return str(d)

    def dump_None(self, d):  # py obj?
        return (
                self.dump_float(d) if isinstance(d, float)
                else d if isinstance(d, (str, dict, int, float))
                else str(d))

    def dump_float(self, d):
        if d == float('inf'):
            return 'Infinity'
        if d == float('-inf'):
            return '-Infinity'
        if d == float('nan'):
            return 'NaN'
        return d
