=================
array contraction
=================

You must have noticed that there are too many unnecessary intermediate
arrays. With precise relationship between statement and array element
at hand, we can find out and eliminate them.

For example, :code:`A` is input, :code:`C` is output, we want to
eliminate B. We assume one statement access to at most one element of
an array here.

.. code::

    ({S1[i] -> B[i] : 0 <= i < 2},
     (var, {S1[i] -> A[i] : 0 <= i < 2}))

    ({S2[i] -> C[i] : 0 <= i < 2},
     (var, {S2[i] -> B[i] : 0 <= i < 2}))


First we find out all intermediate arrays which all its elements has
been used once or less.


.. code::

    def find_contractible():
        reduction_arrays = ctx.fini_stmts.get_assign_map().range()
        use_map = ctx.get_use_map()

        for k, v in ctx.intermediate_arrays.items():
            if not v.intersect(reduction_arrays).is_empty():
                continue

            uses = use_map.intersect_range(v)
            if not uses.is_injective():
                continue

            return k, uses

we get

.. code::

    (S2, {S2[i] -> B[i] : 0 <= i < 2})


Then we find out the statement which defined the element used here.

.. code::

    m, = to_maps(uses.intersect_domain(domain))
    maps = to_maps(m.apply_range(defined_by))

    for stmt_map in maps:
        assert not stmt_map.is_empty()

        stmt_domain = stmt_map.domain()
        name = stmt_domain.get_tuple_name()
        stmt = ctx.def_stmts.get(name, ctx.update_stmts.get(name, None))

.. code::

    ({S1[i] -> B[i] : 0 <= i < 2},
     (var, {S1[i] -> A[i] : 0 <= i < 2}))


Replace B in S2 by definition

.. code::

    {S2[i] -> S1[i] : 0 <= i < 2} * {S1[i] -> A[i] : 0 <= i < 2}
    {S2[i] -> A[i] : 0 < i < 2}


Thus we eliminated B.

.. code::

    ({S2[i] -> C[i] : 0 <= i < 2},
     (var, {S2[i] -> A[i] : 0 <= i < 2}))
