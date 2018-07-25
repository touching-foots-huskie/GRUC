#  keras model is used in trainers.| after trainer added data 
import pdb
from scipy.signal import savgol_filter as filt
import numpy as np
import dataset as D
import tensorflow as tf
from matplotlib import pyplot as plt
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Activation
from keras.layers import CuDNNLSTM
from keras.layers import CuDNNGRU as GRU
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

        self.model.add(GRU(200, input_shape=(None, config['dim']), return_sequences=True, \
        kernel_initializer=init))
        #  self.model.add(CuDNNGRU(64, return_sequences=True, kernel_initializer=init))
        self.model.add(GRU(config['out_dim'], return_sequences=True, kernel_initializer=init))
        
        adam = Adam(lr=config['learning_rate'], clipnorm=1.0)
        #  define learning structure
        #  set session
        set_session(tf.Session(config=gpu_config))

        self.model.compile(loss='mse', optimizer=adam, metrics=['mae'])


    def train(self, dataX, dataY):
        #  get history:
        history = self.model.fit(dataX, dataY, batch_size=self.config['batch_size'], nb_epoch=self.config['training_epochs'], verbose=2, validation_split=0.2)
        return history

    def save(self):
        if  self.config['mode'] == 'res_train':
            self.model.save_weights('train_log/{}_res_model.h5'.format(self.config['plant']))
        else:
            self.model.save_weights('train_log/{}_model.h5'.format(self.config['plant']))
            print('model saved!')

    def restore(self):
        if  self.config['mode'] == 'res_test' or self.config['mode'] == 'res_train':
            self.model.load_weights('train_log/{}_res_model.h5'.format(self.config['plant']))
        else:
            print('I am going to load {}'.format(self.config['plant']))
            self.model.load_weights('train_log/{}_model.h5'.format(self.config['plant']))
        print('model loaded!')

    def validate(self, val_dataX, val_dataY):
        print('Start validate!')
        print(val_dataX.shape)
        predict_Y = self.model.predict(val_dataX)
        for i in range(val_dataX.shape[0]):
            #  plt.plot(val_dataX[i, :, 1], label='A')
            #  plt.plot(val_dataX[i, :, 2], label='J')
            plt.plot(predict_Y[i].ravel(), label='prediction')
            plt.plot(val_dataY[i].ravel(), label='actual')
            #  smooth:
            '''
            sig = val_dataY[i].ravel()
            sig = filt(sig, 51, 5) 
            plt.plot(sig, label='smooth')
            '''
            #  d_index, d_val_dataY = D.down_sample(val_dataY[i], 10)
            #  plt.plot(d_index, d_val_dataY, label='d')
            plt.legend()
            plt.show()

    def implement(self, im_dataX):
        predict_Y = self.model.predict(im_dataX)
        predict_Y = predict_Y.reshape([predict_Y.shape[0], -1, 1])
        return predict_Y


if __name__ == '__main__':
    main()
