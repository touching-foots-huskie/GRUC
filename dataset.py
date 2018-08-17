# : Harvey Chang
# : chnme40cs@gmail.com
#  this file is used to describe the non-linear plant for learning:
import pdb
import tqdm
import random
import numpy as np
import scipy.io as scio
from matplotlib import pyplot as plt
from sklearn.utils import shuffle


def read_mat(filename):
    #  different scales in data:
    data = scio.loadmat(filename)
    if 'x' in data.keys():
        data = data['x']
        data = data * 1.0
    elif 'y' in data.keys():
        data = data['y']
        data = data
    else:
        print('wrong data structure.')
    return data


def read_data(file_path, config):

    dataX = read_mat('{}/x.mat'.format(file_path))
    dataY = read_mat('{}/y.mat'.format(file_path))
    print('data shape is {}'.format(dataX.shape))
    #  rescale into [-1, 1]
    dataX, dataY = shuffle(dataX, dataY)
    #  get training and get validation set:
    return dataX, dataY


def xy_process(X, Y, config):
    #  used in learning
    #  differential structure
    if len(X.shape) == 1:
        X = X[:, np.newaxis] 
    if len(Y.shape) == 1:
        Y = Y[:, np.newaxis]

    if config['diff']:
        Vm = X[1:] - X[:-1] 
        A = (Vm[1:] - Vm[:-1]) 
        V = (X[2:] - X[:-2])
        J = A[2:] - A[:-2]
        #  clip:
        A = A[1:-1]
        V = V[1:-1]
        # shape of new datax in 4 shorter [2:-2]
        X = np.concatenate([X[2:-2], V, A, J], axis=-1)

        Y = Y[2:-2]

    #  get scaled:
    for i in range(X.shape[-1]):
        X[:, i] *= config['scales'][i]

    Y *= config['scales'][-1]

    '''
    print('X: {}'.format(X[:, 0].max()))
    print('V: {}'.format(X[:, 1].max()))
    print('A: {}'.format(X[:, 2].max()))
    print('J: {}'.format(X[:, 3].max()))
    print('Y: {}'.format(Y.max()))
    '''

    #  get tuples:
    datax = np.asarray(X, dtype=np.float32)
    datay = np.asarray(Y, dtype=np.float32)

    return datax, datay


def x_process(X, config):
    #  used in implementation
    #  get differ structure X
    dataX = []
    for i in range(X.shape[0]):
        #  differential structure
        if len(X.shape) == 3:
           Xm = X[i]
        else:
           Xm = X[i].reshape([-1, 1])

        if config['diff']:
            Vm = Xm[1:] - Xm[:-1] 
            A = (Vm[1:] - Vm[:-1]) 
            V = (Xm[2:] - Xm[:-2])
            J = A[2:] - A[:-2]
            #  clip:
            A = A[1:-1]
            V = V[1:-1]
            # shape of new datax in 4 shorter [2:-2]
            # Xm = np.concatenate([V, A, J], axis=-1)
            Xm = np.concatenate([X[0, 2:-2], V, A, J], axis=-1)

        #  get scaled:
        for k in range(Xm.shape[-1]):
            Xm[:, k] *= config['scales'][k]

        #  time connected
        datax = np.asarray(Xm, dtype=np.float32)
        dataX.append(datax)
    #  cast:
    dataX = np.asarray(dataX)
    return dataX


def down_sample(X, sample_rate, axis=0):
    leng = X.shape[axis]
    index = np.array(range(leng//sample_rate))*sample_rate
    return index, np.take(X, index, axis=axis)


if __name__ == "__main__":
    pass

