class Symbol(object):
    required_fields = ()

    def __init__(self, position, **kwargs):
        self.position = position

        assert all((k in kwargs) for k in self.required_fields)

        for k,v in kwargs.items():
            self.__dict__[k] = v


class Argument(Symbol):
    required_fields = ('type', 'shape')

class Monad(Symbol):
    required_fields = ('rank', 'expr')

class Dyad(Symbol):
    required_fields = ('rank', 'expr')


class Literal(Symbol):
    required_fields = ('shape', 'body')

class ApplyMonad(Symbol):
    required_fields = ('shape', 'op', 'rank', 'y')

class ApplyDyad(Symbol):
    required_fields = ('shape', 'op', 'rank', 'x', 'y')


class Table(object):

    def __init__(self, default):
        self.next_var_id = 0
        self.declarations = {}
        self.vars = {}
        self.symbols = default.copy()

    def check_shape(self, name):
        v = self.symbols[name]
        assert self.declarations[name].shape == self.vars[v].shape, "shape of symbol '%s' does not match with declaration" % (name,)

    def add_declaration(self, name, value):
        assert name not in self.declarations, "'%s' already declared" % (name,)
        self.declarations[name] = value

        if name in self.symbols:
            self.check_shape(name)

    def add_var(self, value):
        name = "v"+str(self.next_var_id)
        self.next_var_id += 1
        self.vars[name] = value
        return name

    def itervars(self):
        for i in xrange(self.next_var_id):
            yield "v" + str(i)

    def add_symbol(self, name, value):
        assert name not in self.symbols, "symbol '%s' already defined" % (name,)
        self.symbols[name] = value

        if name in self.declarations:
            self.check_shape(name)

    def get_symbol(self, name):
        v = self.symbols.get(name, None)
        if v is None:
            d = self.declarations.get(name, None)
            assert d is not None, "'%s' is not defined" % (name,)
            assert d.type == "in", "'%s' is not input" % (name,)
            v = self.add_var(d)
            self.add_symbol(name, v)
        return v
