==============================
a simple example with autograd
==============================

There are a great number of tutorials on how to build a neural
network. Very sad, most of them are too complicated for me. I don't
see how artificial neural network has anything to do with layers of
neurons. Fortunately, there is autograd, which does not force me to
think in layers.

Let's begin with a simple example [#]_ . For convenience, we will
stick to this example in the first part of this tutorial. But we don't
really use numpy nor autograd in our framework. If you don't want to
install any of them, just skip this and move on.

.. [#] A Step by Step Backpropagation Example (https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/)

Autograd calculates the derivative of a function with respect to its
first argument only. Thus we have to pack weights and biases into a
tuple.

.. code::

    from autograd import grad, numpy as np

    def sigmoid(x):
        return 1.0/(np.exp(-x) + 1)

    def predict(params, input):
        (W1,B1),(W2,B2) = params
        hidden = sigmoid(np.dot(W1,input) + B1)
        output = sigmoid(np.dot(W2,hidden) + B2)
        return output


the output

.. code::

    W1 = np.array(
        [ [0.15,0.20],
          [0.25,0.30] ])

    B1 = 0.35

    W2 = np.array(
        [ [0.40,0.45],
          [0.50,0.55] ])

    B2 = 0.60

    PARAMS = [(W1,B1),(W2,B2)]

    INPUT = np.array([0.05,0.10])

    assert np.allclose(
        predict(PARAMS, INPUT),
        np.array([0.75136507,0.772928465]))


the loss

.. code::

    def loss(params, input, target):
        return (0.5*(target-predict(params,input))**2).sum()

    TARGET = np.array([0.01,0.99])

    assert np.allclose(
        loss(PARAMS, INPUT, TARGET),
        0.298371109)


the new weights and biases

.. code::

    loss_grad = grad(loss)

    def train(params, input, target):
        (W1,B1),(W2,B2) = params
        (dW1,dB1),(dW2,dB2) = loss_grad(params,input,target)
        return [(W1-0.5*dW1,B1-0.5*dB1),(W2-0.5*dW2,B2-0.5*dB2)]

    (W1,B1),(W2,B2) = train(PARAMS, INPUT, TARGET)

    assert np.allclose(
        W1,
        np.array(
            [ [0.149780716, 0.19956143],
              [0.24975114, 0.29950229]]))

    assert np.allclose(
        W2,
        np.array(
            [ [0.35891648, 0.408666186],
              [0.511301270, 0.561370121]]))

As you see, just simple formulas and optimization with gradient based
method, no layers are required.
