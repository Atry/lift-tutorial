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


First, let's define Array and ArrayView.

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

        def __eq__(self, other):
            return (self.shape == other.shape) and (self.data == other.data)


This is a multidimensional array in C.

.. code::

    int a[2][3] = {{1,2,3},{4,5,6}};


And this is the equivalent array in LiFT.

.. code::

    Array((3,2),[1,2,3,4,5,6])

monad

.. code::

    def product(l):
        x = 1
        for e in l:
            x *= e
        return x

    def interp_monad(op, ry, y):
        if ry is None:
            ry = len(y.shape)

        shape = op.get_shape(y.shape[:ry]) + y.shape[ry:]
        z = Array(shape, [0.0 for _ in xrange(product(shape))])

        vy = y.view()
        vz = z.view()

        p = product(y.shape[ry:])
        for i in xrange(p):
            op.interp(y.shape[:ry], vy.subview(i,p), vz.subview(i,p))

        return z

sum

.. code::

    class Sum(object):
        rank = None

        def get_shape(self, sy):
            return sy[:-1]

        def interp(self, sy, vy, vz):
            p = product(sy[:-1])
            for i in xrange(p):
                vz[i] = 0

            for i in xrange(sy[-1]):
                vyi = vy.subview(i, sy[-1])
                for j in xrange(p):
                    vz[j] += vyi[j]

    assert interp_monad(Sum(), 1, Array((2,),[1,2])) == Array((),[3])
    assert interp_monad(Sum(), 1, Array((3,),[1,2,3])) == Array((),[6])

    assert interp_monad(Sum(), 1, Array((2,2),[1,2,3,4])) == Array((2,),[3,7])
    assert interp_monad(Sum(), 2, Array((2,2),[1,2,3,4])) == Array((2,),[4,6])
