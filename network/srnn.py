#  keras model is used in trainers.| after trainer added data 
import pdb
import numpy as np
import dataset as D
import tensorflow as tf
import network.sru as sru
from matplotlib import pyplot as plt
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Activation
from keras.layers import CuDNNLSTM
from keras.layers import CuDNNGRU
from keras.optimizers import Adam
from keras.initializers import Orthogonal
from keras.backend.tensorflow_backend import set_session


class keras_model:
    def __init__(self, config):
        #  configuration:
        #  set gpu:
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.3, allow_growth=True)
        gpu_config = tf.ConfigProto(gpu_options=gpu_options,allow_soft_placement=True)

        #  other configuration
        self.config = config
        #  define model
        #  gru structure
        self.model = Sequential()
        init = Orthogonal()

        self.model.add(sru(8, input_shape=(None, config['dim']*self.config['m']), return_sequences=True, \
        kernel_initializer=init))
        #  self.model.add(CuDNNGRU(64, return_sequences=True, kernel_initializer=init))
        self.model.add(sru(config['out_dim'], return_sequences=True, kernel_initializer=init))
        
        adam = Adam(lr=config['learning_rate'], clipnorm=1.0)
        #  define learning structure
        #  set session
        set_session(tf.Session(config=gpu_config))

        self.model.compile(loss='mae', optimizer=adam, metrics=['mae'])


    def train(self, dataX, dataY):
        self.model.fit(dataX, dataY, batch_size=self.config['batch_size'], nb_epoch=self.config['training_epochs'], verbose=2, validation_split=0.2)

    def save(self):
        self.model.save_weights('train_log/{}_model.h5'.format(self.config['plant']))
        print('model saved!')

    def restore(self):
        self.model.load_weights('train_log/{}_model.h5'.format(self.config['plant']))
        print('model loaded!')

    def validate(self, val_dataX, val_dataY):
        print('Start validate!')
        print(val_dataX.shape)
        predict_Y = self.model.predict(val_dataX)
        for i in range(val_dataX.shape[0]):
            plt.plot(val_dataX[i, :, 0], label='V')
            plt.plot(np.sin(val_dataX[i, :, 0]), label='S')

            #  plt.plot(val_dataX[i, :, 1], label='A')
            #  plt.plot(val_dataX[i, :, 2], label='J')
            plt.plot(predict_Y[i], label='prediction')
            plt.plot(val_dataY[i], label='actual')
            d_index, d_val_dataY = D.down_sample(val_dataY[i], 10)
            plt.plot(d_index, d_val_dataY, label='d')
            plt.legend()
            plt.show()

    def implement(self, im_dataX):
        predict_Y = self.model.predict(im_dataX)
        return predict_Y


if __name__ == '__main__':
    main()
