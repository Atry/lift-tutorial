==============
shape checking
==============

declare inputs and outputs with their shapes.

.. code::

    Input :: (in 2)
    W1 :: (in 2 2)
    B1 :: (in)
    W2 :: (in 2 2)
    B2 :: (in)
    Output :: (out 2)


Unlike J, we use rank to distinguish between definition of monad, dyad
and array. We don't have operator precedence in LiFT. You should
always use parenthesis. This is why it is lisp flavoured.

.. code::

    sigmoid"0 := (1 / ((exp (0 - y)) + 1))
    dot"1 1 := ((reduce 1 +) (x * y))

    Hidden := (sigmoid ((W1 dot Input) + B1))
    Output := (sigmoid ((W2 dot Hidden) + B2))

In the definition of a monad, :code:`y` means the argument. While in
the definition of a dyad, :code:`x` means the left argument, :code:`y`
means the right argument.

We have extended reduce (called insert in J) to multiple
dimensions. :code:`(reduce 1 +)` means 1-dimension reduce, is
equivalent to :code:`+/` of J.

Shape is checked when a new declaration or definition added to symbol
table. If we could not find a symbol in the symbols, we would try to
find it in the declarations, see if it is an input.

.. code::

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


We use the same :code:`Array`, :code:`interp_monad`,
:code:`interp_dyad` as :code:`rank.py` here. So after shape checking,
we transform the statements into a simpler form which is also required
by our implementation of reverse mode automatic differentiation.

Let's calculate the output.

.. code::

    from lift1.parser import Parser
    from lift1.check import check_stmts
    from lift1.interp import interp
    from lift1.interp import Array

    p = Parser(filename='<string>')

    SOURCE = (
    """
    Input :: (in 2)
    W1 :: (in 2 2)
    B1 :: (in)
    W2 :: (in 2 2)
    B2 :: (in)
    Output :: (out 2)

    sigmoid"0 := (1 / ((exp (0 - y)) + 1))
    dot"1 1 := ((reduce 1 +) (x * y))

    Hidden := (sigmoid ((W1 dot Input) + B1))
    Output := (sigmoid ((W2 dot Hidden) + B2))
    """)


    table = check_stmts(p.parse(SOURCE))
    values = interp(
        table,
        W1 = Array((2,2), [0.15,0.20,0.25,0.30]),
        B1 = Array((), [0.35]),
        W2 = Array((2,2), [0.40,0.45,0.50,0.55]),
        B2 = Array((), [0.60]),
        Input = Array((2,), [0.05,0.10]))

    assert (values[table.symbols["Output"]]
            .allclose(Array((2,), [0.75136507,0.772928465])))
