=========================
automatic differentiation
=========================

There are many good introductions to automatic differentiation you can
find on the internet, but few of them talks about reverse mode
automatic differentiation. Reverse mode is just as simple as forward
mode.

A very simple example with only monad.

.. math::

    \begin{array}{rcl}
    v_2 &=& f(v_1) \\
    v_3 &=& g(v_2) \\
    v_4 &=& h(v_3) \\
    \end{array}

:math:`\frac{\partial v_4}{\partial v_1} = \frac{\partial v_4}{\partial v_3} \cdot \frac{\partial v_3}{\partial v_2} \cdot \frac{\partial v_2}{\partial v_1}`

.. math::

    \begin{array}
    v_5 &=& \frac{\partial v_4}{\partial v_3} \\
    v_6 &=& v_5 \cdot \frac{\partial v_3}{\partial v_2} \\
    v_7 &=& v_6 \cdot \frac{\partial v_2}{\partial v_1} = \frac{\partial v_4}{\partial v_3} \cdot \frac{\partial v_3}{\partial v_2} \cdot \frac{\partial v_2}{\partial v_1} = \frac{\partial v_4}{\partial v_1} \\
    \end{array}


dyad

.. math::

    \begin{array}{rcl}
    v_2 &=& f(v_1) \\
    v_3 &=& g(v_1) \\
    v_4 &=& v_2 + v_3 \\
    v_5 &=& h(v_4) \\
    v_6 &=& i(v_5) \\
    \end{array}


:math:`\frac{\partial v_6}{\partial v_5} \cdot \frac{\partial v_5}{\partial v_4} \cdot (\frac{\partial v4}{\partial v2} \cdot \frac{\partial v2}{\partial v1} + \frac{\partial v4}{\partial v3} \cdot \frac{\partial v3}{\partial v1})`


.. math::

    \begin{array}{rcl}
    v_7 &=& \frac{\partial v_6}{\partial v5} \\
    v_8 &=& \frac{\partial v_5}{\partial v4} \\
    v_9 &=& \frac{\partial v_6}{\partial v4} = v_8 \cdot v_7 \\
    v_{10} &=& \frac{\partial v_4}{\partial v_2} = 1\\
    v_{11} &=& \frac{\partial v_6}{\partial v_2} = v_9 \cdot v_{10} \\
    v_{12} &=& \frac{\partial v_2}{\partial v_1} \\
    v_{13} &=& v_{11} \cdot v_{12} \\
    v_{14} &=& \frac{\partial v_4}{\partial v_3} = 1\\
    v_{15} &=& \frac{\partial v_6}{\partial v_3} = v_{9} \cdot v_{14} \\
    v_{16} &=& \frac{\partial v_3}{\partial v_1} \\
    v_{17} &=& v_{15} \cdot v_{16} \\
    v_{18} &=& v_{13} + v_{17} \\
    \end{array}
