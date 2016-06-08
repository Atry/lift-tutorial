import autograd.numpy as np
from autograd import grad

def sigmoid(x):
    return 1.0/(np.exp(-x) + 1)

def predict(params,input):
    (W1,B1),(W2,B2) = params
    hidden = sigmoid(np.dot(W1,input) + B1)
    output = sigmoid(np.dot(W2,hidden) + B2)
    return output

def loss(params,input,target):
    return (0.5*(target-predict(params,input))**2).sum()

loss_grad = grad(loss)

def train(params, input, target):
    grad = loss_grad(params,input,target)
    return [(W-0.5*dW,B-0.5*dB) for ((dW,dB),(W,B)) in zip(grad,params)]

W1 = np.array(
    [ [0.15,0.20],
      [0.25,0.30]])

B1 = 0.35

W2 = np.array(
    [ [0.40,0.45],
      [0.50,0.55]])

B2 = 0.60

PARAMS = [(W1,B1),(W2,B2)]
INPUT = np.array([0.05,0.10])
TARGET = np.array([0.01,0.99])

PARAMS = train(PARAMS,INPUT,TARGET)
