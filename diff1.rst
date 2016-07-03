=========================
automatic differentiation
=========================

There are many good introductions to automatic differentiation you can
find on the internet. But many of them talk about forward mode only,
the others simply explain the tape structure which is for control
structures. Since LiFT does not have any control structure,
implementation of reverse mode could be as easy as forward mode.

A simple example with only monads. :math:`z = h(g(f(y)))` . First, we
rewrite the equation, so that there is only one monad in each
statement.

.. math::

    \begin{array}{rcl}
    v_2 &=& f(v_1) \\
    v_3 &=& g(v_2) \\
    v_4 &=& h(v_3) \\
    \end{array}


Then we follow the chain rule from outside to inside.

.. math::

    \begin{array}{rcl}
    v_5 &=& \frac{\partial v_4}{\partial v_3} \\
    v_6 &=& v_5 \cdot \frac{\partial v_3}{\partial v_2} = \frac{\partial v_4}{\partial v_3} \cdot \frac{\partial v_3}{\partial v_2} \\
    v_7 &=& v_6 \cdot \frac{\partial v_2}{\partial v_1} = \frac{\partial v_4}{\partial v_3} \cdot \frac{\partial v_3}{\partial v_2} \cdot \frac{\partial v_2}{\partial v_1} = \frac{\partial v_4}{\partial v_1}
    \end{array}



An example with dyad, :math:`i(h(f(x) + g(x)))`

.. math::

    \begin{array}{rcl}
    v_2 &=& f(v_1) \\
    v_3 &=& g(v_1) \\
    v_4 &=& v_2 + v_3 \\
    v_5 &=& h(v_4) \\
    v_6 &=& i(v_5) \\
    \end{array}


calculation split into two branches since :math:`v_4` .

.. math::

    \begin{array}{rcl}
    v_7 &=& \frac{\partial v_6}{\partial v_5} \\
    v_8 &=& v_7 \cdot \frac{\partial v_5}{\partial v_4} = \frac{\partial v_6}{\partial v_5} \cdot \frac{\partial v_5}{\partial v_4} \\
    v_9 &=& v_8 \cdot \frac{\partial v_4}{\partial v_2} = \frac{\partial v_6}{\partial v_5} \cdot \frac{\partial v_5}{\partial v_4} \cdot \frac{\partial v_4}{\partial v_2} \\
    v_{10} &=& v_9 \cdot \frac{\partial v_2}{\partial v_1} = \frac{\partial v_6}{\partial v_5} \cdot \frac{\partial v_5}{\partial v_4} \cdot \frac{\partial v_4}{\partial v_2} \cdot \frac{\partial v_2}{\partial v_1} \\
    v_{11} &=& v_8 \cdot \frac{\partial v_4}{\partial v_3} = \frac{\partial v_6}{\partial v_5} \cdot \frac{\partial v_5}{\partial v_4} \cdot \frac{\partial v_4}{\partial v_3} \\
    v_{12} &=& v_{11} \cdot \frac{\partial v_3}{\partial v_1} = \frac{\partial v_6}{\partial v_5} \cdot \frac{\partial v_5}{\partial v_4} \cdot \frac{\partial v_4}{\partial v_3} \cdot \frac{\partial v_3}{\partial v_1} \\
    v_{13} &=& v_{11} + v_{12} = \frac{\partial v_6}{\partial v_5} \cdot \frac{\partial v_5}{\partial v_4} \cdot \frac{\partial v_4}{\partial v_2} \cdot \frac{\partial v_2}{\partial v_1} + \frac{\partial v_6}{\partial v_5} \cdot \frac{\partial v_5}{\partial v_4} \cdot \frac{\partial v_4}{\partial v_3} \cdot \frac{\partial v_3}{\partial v_1} = \frac{\partial v_6}{\partial v_1} \\
    \end{array}


We write expressions in prefix notation.

.. code::

    1 + 2     ->  ('+',  1,   2)
    v1 + v2   ->  ('+', 'v1', 'v2')
    sin(v1)   ->  ('sin', 'v1')


To reduce duplication, we will apply these rules before adding new
variable, and will return the same variable id for same definition.

.. code::

    add(+, 0, x) -> x
    add(+, x, 0) -> x
    add(*, 1, x) -> x
    add(*, x, 1) -> x
    add(*, 0, x) -> 0
    add(*, x, 0) -> 0



.. code::

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


Differentiation is simply implemented by applying differentiation rules.

.. code::

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


An example taken from wikipedia, :math:`z = (\sin x) + (x \cdot y)`

.. code::

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
