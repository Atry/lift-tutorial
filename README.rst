=========================================
Rolling your own neural network framework
=========================================

We are going to build a neural network framework called LiFT. LiFT
stands for LIsp-Flavoured Tensor, following the trend of `LFE`__ in
naming. As pointed out by Phil Karlton, there are only two hard things
in Computer Science: cache invalidation and naming things. LFE has
made naming a lot easier. If you are working on something inspired by
X and Y, and cannot think of a good name, just call it X Flavoured Y,
problem solved.

We show throughout this tutorial, by adopting rank of function from J
and piggybacking on integer set library, a neural network framework
could be built with much less effort.

LiFT can be served as a good starting point of your full-fledged
neural network framework. And LiFT does not limit itself to neural
network, it could also be a good choice if you need tensor and
gradient based optimization.

.. __: http://lfe.io/

* `a simple example with autograd <autograd.rst>`_
* `tensor and rank <rank.rst>`_
* `automatic differentiation <diff1.rst>`_
* `shape checking <shape.rst>`_
* `backpropagation <diff2.rst>`_
* `compilation with integer set library <isl.rst>`_
* `array contraction <contract.rst>`_
* `convolution <conv.rst>`_

If you have any questions, find any mistakes or have any suggestions,
feel free to open an `issue`__ or send a pull request.

.. __: https://github.com/bhuztez/lift-tutorial/issues
