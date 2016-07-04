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


class Sum(object):
    rank = None

    def get_shape(self, sy):
        return sy[:-1]

    def interp(self, sy, vy, vz):
        p = product(sy[:-1])
        for i in xrange(p):
            vz[i] = 0

        for i in xrange(sy[-1]):
            vyi = vy.subview(i, sy[-1])
            for j in xrange(p):
                vz[j] += vyi[j]


def product(l):
    x = 1
    for e in l:
        x *= e
    return x


def interp_monad(op, ry, y):
    shape = op.get_shape(y.shape[:ry]) + y.shape[ry:]
    z = Array(shape, [0.0 for _ in xrange(product(shape))])

    vy = y.view()
    vz = z.view()

    p = product(y.shape[ry:])
    for i in xrange(p):
        op.interp(y.shape[:ry], vy.subview(i,p), vz.subview(i,p))

    return z


assert interp_monad(Sum(), 1, Array((3,),[1,2,3])) == Array((),[6])
assert interp_monad(Sum(), 2, Array((3,2),[1,2,3,4,5,6])) == Array((3,),[5,7,9])
assert interp_monad(Sum(), 1, Array((3,2),[1,2,3,4,5,6])) == Array((2,),[6,15])


def get_shape_monad(op, ranks, sy):
    if not ranks:
        ry = op.rank
        inner = op.get_shape
    else:
        ry = ranks[-1]

        def inner(sy):
            return get_shape_monad(op, ranks[:-1], sy)

    if ry is None:
        ry = len(sy)

    return inner(sy[:ry]) + sy[ry:]


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


def rankex1(op, ranks, y):
    shape = get_shape_monad(op, ranks, y.shape)
    z = Array(shape, [0.0 for _ in xrange(product(shape))])
    interp_monad(op, ranks, y.shape, y.view(), z.view())
    return z


assert rankex1(Sum(), (), Array((3,),[1,2,3])) == Array((),[6])
assert rankex1(Sum(), (), Array((3,2),[1,2,3,4,5,6])) == Array((3,),[5,7,9])
assert rankex1(Sum(), (1,), Array((3,2),[1,2,3,4,5,6])) == Array((2,),[6,15])


def agree(sx, sy):
    assert all(a==b for a,b in zip(reversed(sx),reversed(sy)))
    return sx if len(sx) >= len(sy) else sy


def get_shape_dyad(op, ranks, sx, sy):
    if not ranks:
        rx, ry = op.rank
        inner = op.get_shape
    else:
        rx, ry = ranks[-1]
        def inner(sx, sy):
            return get_shape_dyad(op, ranks[:-1], sx, sy)

    if rx is None:
        rx = len(sx)
    if ry is None:
        ry = len(sy)

    return inner(sx[:rx], sy[:ry]) + agree(sx[rx:], sy[ry:])


def interp_dyad(op, ranks, sx, vx, sy, vy, vz):
    if not ranks:
        rx, ry = op.rank
        inner = op.interp
    else:
        rx, ry = ranks[-1]
        def inner(sx, vx, sy, vy, vz):
            interp_dyad(op, ranks[:-1], sx, vx, sy, vy, vz)

    if rx is None:
        rx = len(x.shape)

    if ry is None:
        ry = len(y.shape)

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


def rankex2(op, ranks, x, y):
    shape = get_shape_dyad(op, ranks, x.shape, y.shape)
    z = Array(shape, [0.0 for _ in xrange(product(shape))])
    interp_dyad(op, ranks, x.shape, x.view(), y.shape, y.view(), z.view())
    return z


class Plus(object):
    rank = (0,0)

    def get_shape(self, sx, sy):
        return ()

    def interp(self, sx, vx, sy, vy, vz):
        vz[0] = vx[0] + vy[0]


assert rankex2(Plus(), (), Array((2,),[1,2]), Array((2,),[3,4])) == Array((2,),[4,6])
assert rankex2(Plus(), ((0,1),), Array((2,),[1,3]), Array((2,),[3,4])) == Array((2,2),[4,5,6,7])
