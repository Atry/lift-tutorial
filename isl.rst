====================================
compilation with integer set library
====================================

We use `integer set library`__ and `islpy`__ a python binding of isl
in compilation.

.. __: http://isl.gforge.inria.fr/
.. __: https://pypi.python.org/pypi/islpy

We use set in isl to represent arrays and statements. For example,
an array of shape :code:`(2,3,4)`

.. code::

     {A[i,j,k] : 0 <= i < 4, 0 <= j < 3, 0 <= k < 2 }


We use map to respresent elements of arrays used in statements, to
keep track of precise relationship between elements of arrays and
statements. For example, :code:`C = A + B`

.. code::

     ({S[i] -> C[i] : 0 <= i < 2},
      (call, +,
       (var, {S[i] -> A[i] : 0 <= i < 2}),
       (var, {S[i] -> B[i] : 0 <= i < 2})))

And for reduction, :code:`B = (reduce 1 +) A`

.. code::

     init
     ({S1[] -> B[]}, (const, 0.0))

     update
     ({S2[i] -> B[] : 0 <= i < 2},
      (call, +,
       (var, {S2[i] -> B[] : 0 <= i < 2}),
       (var, {S2[i] -> A[i] : 0 <= i < 2}))
     )

     fini
     ({S3[] -> B[]}, (var, {S3[] -> B[]}))


So actually, this transformation is easier to implement than
interpretation. For example, :code:`compile_monad`

.. code::

    def compile_monad(ctx, op, ranks, sy, y, z):
        if not ranks:
            ry = op.rank
            inner = op.compile
        else:
            ry = ranks[-1]
            def inner(ctx, sy, y, z):
                compile_monad(ctx, op, ranks[:-1], sy, y, z)

        if ry is None:
            ry = len(sy)

        for s in sy[ry:][::-1]:
            y = ctx.append_dim2(y, s)
            z = ctx.append_dim2(z, s)

        inner(ctx, sy[:ry], y, z)


Once all statements are transformed, we use integer set library to
compute a schedule, which will assign a time to each statement. So
that we know when should execute a statement. All use of an element of
a array should be scheduled after it is defined. For reduction arrays,
update statements should be scheduled after init statements, and fini
statements should be scheduled after update statements. Then we use
the schedule to build AST, and expand all statements with their
definitions.
