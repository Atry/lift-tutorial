import islpy as isl
from .utils import product


class Plus(object):
    rank = (0,0)
    zero = 0.0

    def get_shape(self, sx, sy):
        return ()

    def interp(self, sx, vx, sy, vy, vz):
        vz[0] = vx[0] + vy[0]

    def interp_acc_x(self, sx, vx, sy, vy, vz, acc, vg):
        vg[0] += acc[0]

    def interp_acc_y(self, sx, vx, sy, vy, vz, acc, vg):
        vg[0] += acc[0]

    def compile(self, ctx, sx, x, sy, y, z):
        ctx.def_stmts.add(
            (z,
             ('call', '+',
              (('var',x),
               ('var',y)))))

    def compile_update(self, ctx, sx, x, sy, y, z):
        ctx.update_stmts.add(
            (z,
             ('call', '+',
              (('var',x),
               ('var',y)))))

    def compile_acc_x(self, ctx, sx, x, sy, y, z, acc, g):
        ctx.update_stmts.add(
            (g,
             ('call', '+',
              ( ('var', g),
                ('var', acc)
              ))
            ))

    def compile_acc_y(self, ctx, sx, x, sy, y, z, acc, g):
        ctx.update_stmts.add(
            (g,
             ('call', '+',
              ( ('var', g),
                ('var', acc)
              ))
            ))


class Minus(object):
    rank = (0,0)

    def get_shape(self, sx, sy):
        return ()

    def interp(self, sx, vx, sy, vy, vz):
        vz[0] = vx[0] - vy[0]

    def interp_acc_x(self, sx, vx, sy, vy, vz, acc, vg):
        vg[0] += acc[0]

    def interp_acc_y(self, sx, vx, sy, vy, vz, acc, vg):
        vg[0] += -acc[0]

    def compile(self, ctx, sx, x, sy, y, z):
        ctx.def_stmts.add(
            (z,
             ('call', '-',
              (('var',x),
               ('var',y)))))

    def compile_acc_x(self, ctx, sx, x, sy, y, z, acc, g):
        ctx.update_stmts.add(
            (g,
             ('call', '+',
              ( ('var', g),
                ('var', acc)
              ))
            ))

    def compile_acc_y(self, ctx, sx, x, sy, y, z, acc, g):
        ctx.update_stmts.add(
            (g,
             ('call', '+',
              ( ('var', g),
                ('call', '_', (('var', acc),))
              ))
            ))


class Multiply(object):
    rank = (0,0)

    def get_shape(self, sx, sy):
        return ()

    def interp(self, sx, vx, sy, vy, vz):
        vz[0] = vx[0] * vy[0]

    def interp_acc_x(self, sx, vx, sy, vy, vz, acc, vg):
        vg[0] += acc[0] * vy[0]

    def interp_acc_y(self, sx, vx, sy, vy, vz, acc, vg):
        vg[0] += acc[0] * vx[0]

    def compile(self, ctx, sx, x, sy, y, z):
        ctx.def_stmts.add(
            (z,
             ('call', '*',
              (('var',x),
               ('var',y)))))

    def compile_acc_x(self, ctx, sx, x, sy, y, z, acc, g):
        ctx.update_stmts.add(
            (g,
             ('call', '+',
              ( ('var', g),
                ('call', '*', (('var', acc), ('var', y)))
              ))
            ))

    def compile_acc_y(self, ctx, sx, x, sy, y, z, acc, g):
        ctx.update_stmts.add(
            (g,
             ('call', '+',
              ( ('var', g),
                ('call', '*', (('var', acc), ('var', x)))
              ))
            ))


class Divide(object):
    rank = (0,0)

    def get_shape(self, sx, sy):
        return ()

    def interp(self, sx, vx, sy, vy, vz):
        vz[0] = vx[0] / vy[0]

    def interp_acc_x(self, sx, vx, sy, vy, vz, acc, vg):
        vg[0] += acc[0] / vy[0]

    def interp_acc_y(self, sx, vx, sy, vy, vz, acc, vg):
        vg[0] -= acc[0] * vx[0] / vy[0] / vy[0]

    def compile(self, ctx, sx, x, sy, y, z):
        ctx.def_stmts.add(
            (z,
             ('call', '/',
              (('var',x),
               ('var',y)))))

    def compile_acc_x(self, ctx, sx, x, sy, y, z, acc, g):
        ctx.update_stmts.add(
            (g,
             ('call', '+',
              ( ('var', g),
                ('call', '/', (('var', acc), ('var', y)))
              ))
            ))

    def compile_acc_y(self, ctx, sx, x, sy, y, z, acc, g):
        ctx.update_stmts.add(
            (g,
             ('call', '+',
              ( ('var', g),
                ('call', '_',
                 (('call', '/',
                   (('call', '*', (('var', acc), ('var', x))),
                    ('call', '*', (('var', y), ('var', y))))),
                 )
                ))
             )))


class Power(object):
    rank = (0,0)

    def get_shape(self, sx, sy):
        return ()

    def interp(self, sx, vx, sy, vy, vz):
        vz[0] = vx[0] ** vy[0]

    def interp_acc_x(self, sx, vx, sy, vy, vz, acc, vg):
        vg[0] += acc[0] * vz[0] * vy[0] / vx[0]

    def compile(self, ctx, sx, x, sy, y, z):
        ctx.def_stmts.add(
            (z,
             ('call', '**',
              (('var',x),
               ('var',y)))))

    def compile_acc_x(self, ctx, sx, x, sy, y, z, acc, g):
        ctx.update_stmts.add(
            (g,
             ('call', '+',
              ( ('var', g),
                ('call', '/',
                 (('call', '*', (('call', '*', (('var', acc), ('var', z))), ('var', y))),
                  ('var', x))
                )
              ))
            ))


class Exp(object):
    rank = 0

    def get_shape(self, sy):
        return ()

    def interp(self, sy, vy, vz):
        from math import exp
        vz[0] = exp(vy[0])

    def interp_acc_y(self, sy, vy, vz, acc, vg):
        vg[0] += acc[0] * vz[0]

    def compile(self, ctx, sy, y, z):
        ctx.def_stmts.add(
            (z,
             ('call', 'exp',
              (('var',y),))))

    def compile_acc_y(self, ctx, sy, y, z, acc, g):
        ctx.update_stmts.add(
            (g,
             ('call', '+',
              ( ('var', g),
                (('call', '*', (('var', acc), ('var', z)))))
             )))


class Log(object):
    rank = 0

    def get_shape(self, sy):
        return ()

    def interp(self, sy, vy, vz):
        from math import log
        vz[0] = log(vy[0])

    def interp_acc_y(self, sy, vy, vz, acc, vg):
        vg[0] += acc[0] / vz[0]

    def compile(self, ctx, sy, y, z):
        ctx.def_stmts.add(
            (z,
             ('call', 'log',
              (('var',y),))))

    def compile_acc_y(self, ctx, sy, y, z, acc, g):
        ctx.update_stmts.add(
            (g,
             ('call', '+',
              ( ('var', g),
                (('call', '/', (('var', acc), ('var', y)))))
             )))


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

    def interp_acc_y(self, sy, vy, vz, acc, vg):
        n = self.n
        p1, p2 = product(sy[:-n]), product(sy[-n:])

        for i in xrange(p2):
            v = vy.subview(i, p2)
            g = vg.subview(i, p2)

            for j in xrange(p1):
                self.op.interp_acc_y((), vz.subview(j, p1), (), v.subview(j, p1), vz.subview(j, p1), acc.subview(j, p1), g.subview(j, p1))

    def compile(self, ctx, sy, y, z):
        n = self.n

        zi = z
        for s in sy[:-n][::-1]:
            zi = ctx.append_dim2(zi, s)

        ctx.init_stmts.add((zi, ('const', self.op.zero)))

        yu, zu = y, z

        for s in sy[-n:][::-1]:
            yu = ctx.append_dim2(yu, s)
            zu = ctx.append_dim1(zu, s)

        for s in sy[:-n][::-1]:
            yu = ctx.append_dim2(yu, s)
            zu = ctx.append_dim2(zu, s)

        self.op.compile_update(ctx, (), zu, (), yu, zu)
        ctx.fini_stmts.add((zi, ('var', zi)))

    def compile_acc_y(self, ctx, sy, y, z, acc, g):
        n = self.n

        for s in sy[-n:][::-1]:
            y = ctx.append_dim2(y, s)
            z = ctx.append_dim1(z, s)
            acc = ctx.append_dim1(acc, s)
            g = ctx.append_dim2(g, s)

        for s in sy[:-n][::-1]:
            y = ctx.append_dim2(y, s)
            z = ctx.append_dim2(z, s)
            acc = ctx.append_dim2(acc, s)
            g = ctx.append_dim2(g, s)

        self.op.compile_acc_y(ctx, (), z, (), y, z, acc, g)



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
