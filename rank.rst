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

    a = Array((3,2),[1,2,3,4,5,6])



Let's take a look at a simple monad, sum. Sum takes an array of rank
:math:`n` as argument, and returns an array of rank :math:`n-1`. For
example,

.. code::

    sum of Array((3,), [1,2,3])
    1 + 2 + 3 = 6

    sum of Array((3,2), [1,2,3,4,5,6])
    1  2  3
    +  +  +
    4  5  6
    -------
    5  7  9

What if we want to calculate sum of each rank-1 array in a rank-2
array.

.. code::

    sum"1 of Array((3,2), [1,2,3,4,5,6])
    1 + 2 + 3 = 6
    4 + 5 + 6 = 15


Sum can be defined like this

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


We first calculate the product of the dimensions, so that we could use
just a single loop.

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



.. code::

    assert interp_monad(Sum(), 1, Array((3,),[1,2,3])) == Array((),[6])
    assert interp_monad(Sum(), 2, Array((3,2),[1,2,3,4,5,6])) == Array((3,),[5,7,9])
    assert interp_monad(Sum(), 1, Array((3,2),[1,2,3,4,5,6])) == Array((2,),[6,15])


As with J, verb(function)s have intrinsic ranks, and you can also
create verb(function)s with different ranks using double-quote. So we
have to support nested ranks, and we use :code:`None` to represent
rank infinity.

.. code::

    def get_shape_monad(op, ranks, sy):
        if not ranks:
            ry = op.rank
            inner = op.get_shape
        else:
            ry = ranks[-1]

            def inner(sy):
                return get_shape_monad(op, ranks[:-1], sy)

        if ry is None:
            ry = len(sy)

        return inner(sy[:ry]) + sy[ry:]


    def interp_monad(op, ranks, sy, vy, vz):
        if not ranks:
            ry = op.rank
            inner = op.interp
        else:
            ry = ranks[-1]
            def inner(sy, vy, vz):
                interp_monad(op, ranks[:-1], sy, vy, vz)

        if ry is None:
            ry = len(sy)

        p = product(sy[ry:])
        for i in xrange(p):
            inner(sy[:ry], vy.subview(i, p),
                  vz.subview(i, p))


    def rankex1(op, ranks, y):
        shape = get_shape_monad(op, ranks, y.shape)
        z = Array(shape, [0.0 for _ in xrange(product(shape))])
        interp_monad(op, ranks, y.shape, y.view(), z.view())
        return z


Since verb(function)s have intrinsic ranks, we don't have specify
ranks in first two examples.

.. code::

    assert rankex1(Sum(), (), Array((3,),[1,2,3])) == Array((),[6])
    assert rankex1(Sum(), (), Array((3,2),[1,2,3,4,5,6])) == Array((3,),[5,7,9])
    assert rankex1(Sum(), (1,), Array((3,2),[1,2,3,4,5,6])) == Array((2,),[6,15])


Similarly, dyad has one rank for the left argument, and another one
for the right. What about the dimensions not taken by dyad. They have
to agree, i.e., 
