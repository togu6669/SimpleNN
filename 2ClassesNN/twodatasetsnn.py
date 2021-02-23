# based on Karpathy libs
# https://github.com/karpathy/convnetjs/tree/master/demo/js/classify2d.js

# breast cancer dataset
# https://www.analyticsvidhya.com/blog/2019/08/detailed-guide-7-loss-functions-machine-learning-python-code/
import numpy as np
import matplotlib.pyplot as plt


# hiperbolic tangens
def tsnh(lgts):
    # y = np.exp(2 * lgts)
    # return (y - 1) / (y + 1)
    return np.tanh(lgts)

# hiperbolic tangens derivative


def dtsnh(lgts):
    return 1 / np.square(np.cosh(lgts))

# softmax activation
def softmax(lgts):
    lgts = lgts - np.max(lgts)
    b = np.exp(lgts)
    out = b / np.sum(b, 0)
    # clip the softmax result to comply with true output values in a loss function
    np.clip(out, 0.01, 0.99, out)
    return out

# softmax derivative
def dsoftmax(lgts):
    s = softmax(lgts).reshape(-1, 1)
    out = np.diagflat(s) - np.dot(s, s.T)
    return out

# binary cross entropy / log loss and its derivative
# good study: https://math.stackexchange.com/questions/2503428/derivative-of-binary-cross-entropy-why-are-my-signs-not-right
# another discussion: https://stats.stackexchange.com/questions/219241/gradient-for-logistic-loss-function#comment420534_219405
# next explanation: https://www.analyticsvidhya.com/blog/2019/08/detailed-guide-7-loss-functions-machine-learning-python-code/
def binCE(y, l): # y and l are 1-element vectors!
    out = -(l*(np.log(y)) + (1-l)*(np.log(1-y))) # chain rule only for the 2nd element 
    return out

def dbinCE (y, l):
    out = (l-y) / y*(1-y)
    return out

def randomdata():
    data = np.zeros((20, 2)) # [20, 2]
    data[:, 0] = np.random.rand(20, 1).reshape(20)

    data[:10, 1] = np.square(data[:10, 0]) - np.random.randn(10, 1).reshape(10)
    data[10:, 1] = - np.square(data[10:, 0]) + \
        np.random.randn(10, 1).reshape(10)

    label = np.zeros((20,2)) # [20, 2]
    for i in range(10):
        label[i, 1] = 1
        label[i+10, 0] = 1
    return data, label

# train
def train(data, label, hw, hb, ow, ob):
    lr = 0.1
    iter = 7000

    acc = np.zeros(iter)
    for i in range(iter):
        for o in range(label.shape[0]-1):
            # forward
            ii = data[o].reshape(data[o].size, 1)

            hz = np.sum(np.dot(hw.T, ii), 1) + hb
            hz = hz.reshape(hz.size, 1)
            ho = tsnh(hz)  # hiperbolic tangens

            oz = np.sum(np.dot(ow.T, ho), 1) + ob
            oo = softmax(oz).reshape(oz.size, 1)

            # backward
            dlo = dbinCE (oo, label[o].reshape(label[o].size, 1)) # binary cross entropy derivative vector [2, 1], resize label to [2, 1]
            dao = dsoftmax(oz) # jacobian 
            ddo = np.dot (dlo.T, dao) # delta
            # delta * logits (z) derivative = weight delta
            dwo = np.dot(ddo.T, ho.T)

            # "loss" of hidden layer: delta of output layer * weights of output layer
            dlh = np.dot(ddo, ow.T)
            dah = dtsnh(hz)
            # delta * logits (z) derivative = weight delta
            dwh = np.dot(dlh.T * dah, ii.T)

            # update - gradient descent
            ow = ow - lr * dwo.T
            hw = hw - lr * dwh.T
            
            # accuracy: abs (oo[0] - label[o][0]) 
            # acc[i] = acc[i] + 


# draws learning squiggle
def test(data, label, hw, hb, ow, ob):
    for o in range(label.size):
        # forward
        ii = data[o].reshape(data[o].size, 1)

        hz = np.sum(np.dot(hw.T, ii), 1) + hb
        hz = hz.reshape(hz.size, 1)
        ho = tsnh(hz)  # hiperbolic tangens

        oz = np.sum(np.dot(ow.T, ho), 1) + ob
        oo = softmax(oz).reshape(oz.size, 1)

        maxv = 0.0
        out = 0
        # our output : the index of the most probable class, so 0 / 1
        for o in range(oo.size):
            if (oo[o] > maxv):
                out = o
                maxv = oo[o]

        print(maxv - label[o])


# main
hw1 = np.random.randn(2, 12)  # input 2 nuerons fc hidden 12 neurons
hb1 = 0.23
ow1 = np.random.randn(12, 2)  # softmax
ob1 = 0.34

dat, lab = randomdata()

# plt.scatter(dat[:10, 0], dat[:10, 1], c='red')
# plt.scatter(dat[10:, 0], dat[10:, 1], c='green')
# plt.show()

train(dat, lab, hw1, hb1, ow1, ob1)
test(dat, lab, hw1, hb1, ow1, ob1)


# test_x = np.array([[0], [2]])
# test_x_b = np.c_[np.ones((2,1)),test_x]
# test_y = np.dot (test_x_b, a)

# plt.plot(test_x, test_y, 'r-')
