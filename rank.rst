===============
tensor and rank
===============

Everybody is talking about tensor these days. Multidimensional array
is called tensor in Torch. Tensorflow has tensor in its name. However,
to them, tensor is just plain multidimensional array. They don't learn
anything useful from tensor analysis like the J programming language
do.

The rank of an array is the number of its dimensions. In J, verbs
(functions) also have ranks [#]_ . Without ranks, loops are almost
impossible to avoid. So, as a great automatic differentiation tool for
numpy, autograd has sophisticated mechanism to support loops. Many
others don't have both, and their functionality is very limited, you
will soon run into a situation when you have to develop your own
layers. Our framework does not rely on numpy, it is better to adopt
ranks, so that it could be flexible with very simple implementation.

.. [#] http://www.jsoftware.com/help/learning/07.htm

First of all, let's define Array and ArrayView.

.. code::

    class ArrayView(object):

        def __init__(self, data, offset, length):
            self.data = data
            self.offset = offset
            self.length = length

        def subview(self, n, blocks):
            return ArrayView(self.data, self.offset+(self.length/blocks)*n, self.length/blocks)

        def __getitem__(self, index):
            assert 0 <= index < self.length
            return self.data[self.offset+index]

        def __setitem__(self, index, value):
            assert 0 <= index < self.length
            self.data[self.offset+index] = value


    class Array(object):

        def __init__(self, shape, data):
            self.shape = shape
            self.data = data

        def view(self):
            return ArrayView(self.data, 0, len(self.data))
