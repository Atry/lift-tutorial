===========
convolution
===========

Rather than a single operator do all the work, we split the
functionality of convolution into a few simple operators.

.. code::

     Conv1 := ((((trim 2 2)"2) (((oblique 2 +)"4) (K1 ((*"2 0)"2 2) Input))) + B1)
     Relu1 := (relu Conv1)
     Pool1 := (((stride 2 2)"2) (((trim 1 1)"2) (((oblique 2 >.)"4) (((duplicate 2 2)"0) Relu1))))


Oblique in LiFT in different direction than in J.

.. code::

    J

    0 1 2
    1 2 3

    LiFT

    1 2 3
    0 1 2

As reduce, oblique has been extended to multiple dimensions, and
compiles to reduction array.

