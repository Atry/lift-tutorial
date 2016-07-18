===========
convolution
===========

Rather than a single operator do all the work, we split the
functionality of convolution into a few simple operators.

.. code::

     Conv1 := ((((trim 2 2)"2) (((oblique 2 +)"4) (K1 ((*"2 0)"2 2) Input))) + B1)


and pooling shares the same operators.

.. code::

     Pool1 := (((stride 2 2)"2) (((trim 1 1)"2) (((oblique 2 >.)"4) (((duplicate 2 2)"0) Relu1))))


Oblique in LiFT in different direction than in J.

.. code::

    J

    0 1 2
    1 2 3

    LiFT

    1 2 3
    0 1 2

As with reduce, oblique has been extended to multiple dimensions, and
compiles to reduction array.

Trim operator cuts from both ends.

.. code::

     (trim 1) 1 2 3 4 5
     2 3 4

     (trim 2) 1 2 3 4 5
     3

Stride

.. code::

    (stride 2) 1 2 3 4 5
    1 3 5
    (stride 4) 1 2 3 4 5
    1 5
