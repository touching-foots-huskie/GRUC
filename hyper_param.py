#  keras model is used in trainers.| after trainer added data 
import pdb
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
from keras.initializers import Orthogonal
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Activation
from keras.layers import CuDNNGRU
from keras.layers import GRU
from keras.optimizers import Adam

#  autokeras:
from hyperopt import Trials, STATUS_OK, tpe
from hyperas import optim
from hyperas.distributions import choice
from keras.backend.tensorflow_backend import set_session


def data():
    # collectting data structure:
    plant = 'pid'
    mode = 'diff'
    if mode == 'train':
        x_train = np.load('{}/data/fast_data/trainX.npy'.format(plant))
        y_train = np.load('{}/data/fast_data/trainY.npy'.format(plant))
        x_test = np.load('{}/data/fast_data/valX.npy'.format(plant))
        y_test = np.load('{}/data/fast_data/valY.npy'.format(plant))
        #  look shape
    elif mode == 'diff':
        x_train = np.load('{}/data/fast_data/diff_X.npy'.format(plant))
        y_train = np.load('{}/data/fast_data/diff_Y.npy'.format(plant))
        x_test = np.load('{}/data/fast_data/val_diff_X.npy'.format(plant))
        y_test = np.load('{}/data/fast_data/val_diff_Y.npy'.format(plant))
    print('x_train shape: {}'.format(x_train.shape))
    print('x_test shape: {}'.format(x_test.shape))
    return x_train, y_train, x_test, y_test


def create_model(x_train, y_train, x_test, y_test):
    #  gpu setting:
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.3, allow_growth=True)
    gpu_config = tf.ConfigProto(gpu_options=gpu_options,allow_soft_placement=True)

    model = Sequential()
    init = Orthogonal() 
    model.add(CuDNNGRU(8, input_shape=(None, 60,), return_sequences=True,
              kernel_initializer=init))

    #  model.add(CuDNNGRU(64, return_sequences=True, kernel_initializer=init))
    #  model.add(CuDNNGRU(64, return_sequences=True, kernel_initializer=init))
    #  model.add(CuDNNGRU(64, return_sequences=True, kernel_initializer=init))
    #  model.add(CuDNNGRU(32, return_sequences=True, kernel_initializer=init))

    model.add(CuDNNGRU(1, return_sequences=True, kernel_initializer=init))
    #  define learning structure
    adam = Adam(lr={{choice([1e-2, 1e-3])}}, clipnorm=1.0)
    #  setting session:
    set_session(tf.Session(config=gpu_config))
    model.compile(loss={{choice(['mae', 'mse'])}}, metrics=['mae'], optimizer=adam)
    #  find best structure in 100 epochs
    model.fit(x_train, y_train, batch_size={{choice([32, 64, 128])}}, epochs=100, verbose=2, validation_data=(x_test, y_test))
    score, maerror = model.evaluate(x_test, y_test, verbose=0)
    print('Test mae:', maerror)
    return {'loss': maerror, 'status': STATUS_OK, 'model': model}
    

if __name__ == '__main__':
    best_run, best_model = optim.minimize(model=create_model, data=data, algo=tpe.suggest, max_evals=5, trials=Trials())

    X_train, Y_train, X_test, Y_test = data()
    print("Evalutation of best performing model:")
    print(best_model.evaluate(X_test, Y_test))
    print("Best performing model chosen hyper-parameters:")
    print(best_run)
