from . import symbol
from .utils import product


class ArrayView(object):

    def __init__(self, data, offset, length):
        self.data = data
        self.offset = offset
        self.length = length

    def subview(self, n, blocks):
        return ArrayView(self.data, self.offset+(self.length/blocks)*n, self.length/blocks)

    def __getitem__(self, index):
        assert 0 <= index < self.length
        return self.data[self.offset+index]

    def __setitem__(self, index, value):
        assert 0 <= index < self.length
        self.data[self.offset+index] = value


class Array(object):

    def __init__(self, shape, data):
        self.shape = shape
        self.data = data

    def view(self):
        return ArrayView(self.data, 0, len(self.data))

    def __eq__(self, other):
        return (self.shape == other.shape) and (self.data == other.data)

    def allclose(self, other):
        return (self.shape == other.shape) and all(round(abs(x-y),7)==0 for x, y in zip(self.data,other.data))


def interp_monad(op, ranks, sy, vy, vz):
    if not ranks:
        ry = op.rank
        inner = op.interp
    else:
        ry = ranks[-1]
        def inner(sy, vy, vz):
            interp_monad(op, ranks[:-1], sy, vy, vz)

    if ry is None:
        ry = len(sy)

    p = product(sy[ry:])
    for i in xrange(p):
        inner(sy[:ry], vy.subview(i, p),
              vz.subview(i, p))


def interp_dyad(op, ranks, sx, vx, sy, vy, vz):
    if not ranks:
        rx, ry = op.rank
        inner = op.interp
    else:
        rx, ry = ranks[-1]
        def inner(sx, vx, sy, vy, vz):
            interp_dyad(op, ranks[:-1], sx, vx, sy, vy, vz)

    if rx is None:
        rx = len(sx)
    if ry is None:
        ry = len(sy)

    sxo, syo = sx[rx:], sy[ry:]
    px, py = product(sxo), product(syo)

    if len(sxo) <= len(syo):
        common = px
        extra = py/common

        for i in xrange(common):
            for j in xrange(extra):
                inner(sx[:rx], vx.subview(i, px),
                      sy[:ry], vy.subview(i*extra+j, py),
                      vz.subview(i*extra+j, py))
    else:
        common = py
        extra = px/common

        for i in xrange(common):
            for j in xrange(extra):
                inner(sx[:rx], vx.subview(i*extra+j, px),
                      sy[:ry], vy.subview(i, py),
                      vz.subview(i*extra+j, px))


def interp(table, **kwargs):
    values = {}

    for k, v in kwargs.items():
        values[table.symbols[k]] = v

    for name in table.itervars():
        if name in values:
            continue

        v = table.vars[name]
        z = Array(v.shape, [0.0 for _ in xrange(product(v.shape))])

        if isinstance(v, symbol.ApplyMonad):
            interp_monad(
                v.op,
                v.rank,
                table.vars[v.y].shape,
                values[v.y].view(),
                z.view())
        elif isinstance(v, symbol.ApplyDyad):
            interp_dyad(
                v.op,
                v.rank,
                table.vars[v.x].shape,
                values[v.x].view(),
                table.vars[v.y].shape,
                values[v.y].view(),
                z.view())
        elif isinstance(v, symbol.Literal):
            z.data = [float(n.n) for n in v.body]
        else:
            raise NotImplementedError

        values[name] = z

    return values
