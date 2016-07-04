===============
backpropagation
===============

Now it's time to calculate gradient. For simplicity, only scalar
variables are allowed, and we calculate the first order derivatives
only.

We use a special declaration :code:`(grad x y)` to represent the
derivative of :code:`x` with respect to :code:`y`.

.. code::

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

    Target :: (in 2)
    Loss :: (out)

    Loss := ((reduce 1 +) (0.5 * ((Target - Output) ** 2)))

    dW1 :: (grad Loss W1)
    dW2 :: (grad Loss W2)

    nW1 :: (out 2 2)
    nW2 :: (out 2 2)

    nW1 := (W1 - (0.5 * dW1))
    nW2 := (W2 - (0.5 * dW2))


Backpropagation is just a kind of reverse mode automatic
differentiation. To calculate the gradient, we use the backpropagation
algorithm here.

.. code::

    def get_use_graph(self, v):
        graph = self.use_graphs.get(v, None)
        if graph is None:
            assert self.vars[v].shape == ()
            graph = {}

            visited = set()
            queue = [v]

            while queue:
                u = queue.pop(0)
                if u in visited:
                    continue
                visited.add(u)
                var = self.vars[u]

                if isinstance(var, ApplyMonad):
                    queue.append(var.y)
                    graph[var.y] = graph.get(var.y,())+((u,'y'),)
                elif isinstance(var, ApplyDyad):
                    queue.append(var.x)
                    queue.append(var.y)
                    graph[var.x] = graph.get(var.x,())+((u,'x'),)
                    graph[var.y] = graph.get(var.y,())+((u,'y'),)
                elif isinstance(var, Literal):
                    pass
                elif isinstance(var, Argument):
                    pass
                else:
                    raise NotImplementedError

            self.use_graphs[v] = graph

        return graph


Unlike those frameworks with layers, only slight modification is
needed to change forward code to backward. For example,
:code:`interp_monad`

.. code::

    def interp_acc_monad(op, ranks, sy, vy, vz, acc, vg):
        if not ranks:
            ry = op.rank
            inner = op.interp_acc_y
        else:
            ry = ranks[-1]
            def inner(sy, vy, vz, acc, vg):
                interp_acc_monad(op, ranks[:-1], sy, vy, vz, acc, vg)

        if ry is None:
            ry = len(sy)

        p = product(sy[ry:])
        for i in xrange(p):
            inner(sy[:ry], vy.subview(i, p),
                  vz.subview(i, p),
                  acc.subview(i, p),
                  vg.subview(i, p))

Here is the remaining values.

.. code::

    assert (values[table.symbols["Loss"]]
            .allclose(Array((), [0.298371109])))

    assert (values[table.symbols["nW1"]]
            .allclose(
                Array((2,2),
                      [0.149780716, 0.19956143, 0.24975114, 0.29950229])))

    assert (values[table.symbols["nW2"]]
            .allclose(
                Array((2,2),
                      [0.35891648, 0.408666186, 0.511301270, 0.561370121])))
