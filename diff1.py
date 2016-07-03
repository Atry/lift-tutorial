class Vars(object):

    def __init__(self):
        self.next_var_id = 1
        self.defs = {}
        self.lookup = {}

    def add(self, *v):
        name = self.lookup.get(v, None)
        if name is None:
            if v[0] == '+':
                if v[1] == 0:
                    return v[2]
                elif v[2] == 0:
                    return v[1]
            elif v[0] == '*':
                if v[1] == 1:
                    return v[2]
                elif v[2] == 1:
                    return v[1]
                elif v[1] == 0:
                    return 0
                elif v[2] == 0:
                    return 0

            name = "v" + str(self.next_var_id)
            self.next_var_id += 1

            self.defs[name] = v
            self.lookup[v] = name

        return name

    def __getitem__(self, name):
        return self.defs[name]


def diff(vars, acc, v, w):
    if v == w:
        return acc

    v = vars[v]
    if v[0] == 'in':
        return 0
    elif v[0] == 'sin':
        return diff(vars, vars.add('*', acc, vars.add('cos', v[1])), v[1], w)
    elif v[0] == '+':
        gx = diff(vars, acc, v[1], w)
        gy = diff(vars, acc, v[2], w)
        return vars.add('+', gx, gy)
    elif v[0] == '*':
        gx = diff(vars, vars.add('*', v[2], acc), v[1], w)
        gy = diff(vars, vars.add('*', v[1], acc), v[2], w)
        return vars.add('+', gx, gy)

    raise NotImplementedError


def autodiff(vars, v, *wrt):
    return tuple(diff(vars, 1, v, w) for w in wrt)


# z = (sin x) + (x * y)

vars = Vars()

x = vars.add('in', 'x')
assert x == 'v1'
assert vars['v1'] == ('in', 'x')

y = vars.add('in', 'y')
assert y == 'v2'
assert vars['v2'] == ('in', 'y')

z = vars.add('+', vars.add('*',x,y), vars.add('sin',x))
assert z == 'v5'
assert vars['v3'] == ('*', 'v1', 'v2')
assert vars['v4'] == ('sin', 'v1')
assert vars['v5'] == ('+', 'v3', 'v4')

assert autodiff(vars, z, x, y) ==  ('v7', 'v1')
assert vars['v6'] == ('cos', 'v1')
assert vars['v7'] == ('+', 'v2', 'v6')
