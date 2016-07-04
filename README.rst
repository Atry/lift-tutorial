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

LiFT can be served as a good starting point of your full-fledged
neural network framework. And LiFT does not limit itself to neural
network, it could also be a good choice for other areas which need
tensor and gradient based optimization.

.. __: http://lfe.io/

* `a simple example with autograd <autograd.rst>`__
* `tensor and rank <rank.rst>`__
* `automatic differentiation <diff1.rst>`__
* `shape checking <shape.rst>`__
* `backpropagation <diff2.rst>`__

Compilation

Convolution
