from .utils import product


class Plus(object):
    rank = (0,0)
    zero = 0.0

    def get_shape(self, sx, sy):
        return ()

    def interp(self, sx, vx, sy, vy, vz):
        vz[0] = vx[0] + vy[0]


class Minus(object):
    rank = (0,0)

    def get_shape(self, sx, sy):
        return ()

    def interp(self, sx, vx, sy, vy, vz):
        vz[0] = vx[0] - vy[0]


class Multiply(object):
    rank = (0,0)

    def get_shape(self, sx, sy):
        return ()

    def interp(self, sx, vx, sy, vy, vz):
        vz[0] = vx[0] * vy[0]


class Divide(object):
    rank = (0,0)

    def get_shape(self, sx, sy):
        return ()

    def interp(self, sx, vx, sy, vy, vz):
        vz[0] = vx[0] / vy[0]


class Power(object):
    rank = (0,0)

    def get_shape(self, sx, sy):
        return ()

    def interp(self, sx, vx, sy, vy, vz):
        vz[0] = vx[0] ** vy[0]


class Exp(object):
    rank = 0

    def get_shape(self, sy):
        return ()

    def interp(self, sy, vy, vz):
        from math import exp
        vz[0] = exp(vy[0])


class Log(object):
    rank = 0

    def get_shape(self, sy):
        return ()

    def interp(self, sy, vy, vz):
        from math import log
        vz[0] = log(vy[0])


class Reduce(object):
    rank = None

    def __init__(self, table, args):
        n, name = args
        n, = n.body
        self.n = int(n.n)
        assert self.n >= 1
        op = table.get_symbol(name.s)
        assert op.rank == (0,0)
        assert op.get_shape((),()) == ()
        self.op = op

    def get_shape(self, sy):
        n = self.n
        assert len(sy) >= n
        return sy[:-n]

    def interp(self, sy, vy, vz):
        n = self.n
        p1, p2 = product(sy[:-n]), product(sy[-n:])

        for i in xrange(p1):
            vz[i] = self.op.zero

        for i in xrange(p2):
            v = vy.subview(i, p2)
            for j in xrange(p1):
                self.op.interp((), vz.subview(j,p1), (), v.subview(j,p1), vz.subview(j,p1))


builtins = {
    '+': Plus(),
    '-': Minus(),
    '*': Multiply(),
    '/': Divide(),
    '**': Power(),
    'log': Log(),
    'exp': Exp(),
    'reduce': Reduce,
}
