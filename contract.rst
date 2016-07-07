=================
array contraction
=================

You must have noticed that there are too many unnecessary intermediate
arrays. With precise relationship between statement and array element
at head, we can find out and eliminate them.

For example, :code:`A` is input, :code:`C` is output, we want to
eliminate B.

.. code::

    {S1[i] -> B[i] : 0 <= i < 2} : {S1[i] -> A[i] : 0 <= i < 2}
    {S2[i] -> C[i] : 0 <= i < 2} : {S2[i] -> B[i] : 0 <= i < 2}

First we find out all intermediate arrays which all its elements has
been used once or less.

.. code::

    {B[i] : 0 <= i < 2}

Then we find out all the statements which uses an element of B.

.. code::

    {S2[i] -> C[i] : 0 <= i < 2} : {S2[i] -> B[i] : 0 <= i < 2}

And replace with definition of B.

.. code::

    {S2[i] -> S1[i] : 0 <= i < 2} * {S1[i] -> A[i] : 0 <= i < 2}
    {S2[i] -> A[i] : 0 < i < 2}

Thus we eliminated B.

.. code::

    {S2[i] -> C[i] : 0 <= i < 2} : {S2[i] -> A[i] : 0 <= i < 2}
