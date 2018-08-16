#: Harvey Chang
#: chnme40cs@gmail.com
import pdb
import random
import numpy as np
import dataset as D
import scipy.io as scio
import tensorflow as tf
from network.rnn import keras_model as NN
from scipy.signal import savgol_filter as filt
from tpot import TPOTRegressor 
from matplotlib import pyplot as plt


class Trainer:
    def __init__(self, config):
        self.config = config
        self.nn = NN(config) 

        if self.config['restore']:
            self.nn.restore()

        self.batch_size = config['batch_size']

    def add_raw(self, X, Y, data_type='train'):
        #  smooth y:
        Y = Y.reshape([Y.shape[0], -1])
        Y = np.array([filt(Y[i], 51, 5) for i in range(Y.shape[0])])
        Y = Y.reshape([Y.shape[0], -1, self.config['time_step']])

        if data_type == 'train':
            self.train_dataX = X
            self.train_dataY = Y

        if data_type == 'validation':
            self.val_data = dict()
            self.val_dataX = X
            self.val_dataY = Y
            self.val_data['X'] = self.val_dataX
            self.val_data['Y'] = self.val_dataY

    def add_data(self, X, Y):
        #  generating training data
        #  X shape(N, time_step, dimension)
        #  Y shape(N, time_step, dimension)
        dataX, dataY, init_states = [], [], []
        #  sequence them
        for i in range(X.shape[0]):
            datax, datay = D.xy_process(X[i], Y[i], self.config)
            dataX.append(datax)
            dataY.append(datay)

        #  cast:
        dataX = np.asarray(dataX)
        dataY = np.asarray(dataY)

        if len(dataY.shape) == 2:
            dataY = dataY[:, :, np.newaxis]
            
        #  downsample:
        '''
        _, dataX = D.down_sample(dataX, 10, axis=1)
        _, dataY = D.down_sample(dataY, 10, axis=1)
        '''
        self.train_dataX = dataX
        self.train_dataY = dataY
        np.save('{}/fast_data/trainX.npy'.format(self.config['plant']), self.train_dataX)
        np.save('{}/fast_data/trainY.npy'.format(self.config['plant']), self.train_dataY)

        self.val_data = dict()
        self.val_dataX = dataX[-100:]
        self.val_dataY = dataY[-100:]
        self.val_data['X'] = self.val_dataX
        self.val_data['Y'] = self.val_dataY
        np.save('{}/fast_data/valX.npy'.format(self.config['plant']), self.val_dataX)
        np.save('{}/fast_data/valY.npy'.format(self.config['plant']), self.val_dataY)

    def train(self):
        history = self.nn.train(self.train_dataX, self.train_dataY)
        if self.config['save']:
            self.nn.save()
        plt.plot(history.history['mean_absolute_error'])
        plt.xlabel('epoch')
        plt.ylabel('mae')
        plt.title('mae learning process')
        plt.savefig('ac.png')


        self.test()

    def test(self):
        #  drawing examination
        self.nn.validate(self.val_dataX, self.val_dataY)

    def gendiff(self):
        #  gen the differentiate value over current policy
        #  train part:
        predict_Y = self.nn.implement(self.train_dataX)
        diff_Y = self.train_dataY - predict_Y
        #  remove overrange pair:
        overrange = np.argwhere(np.max(diff_Y, axis=1)>0.3)[:, 0]
        diff_Y = np.delete(diff_Y, overrange, axis=0)*3.0
        train_dataX = np.delete(self.train_dataX, overrange, axis=0)
        #  downsample:
        pdb.set_trace()
        #  _, diff_Y = D.down_sample(diff_Y, 10, 1)
        #  _, train_dataX = D.down_sample(train_dataX, 10, 1)
        print(diff_Y.shape)

        np.save('{}/fast_data/diff_X.npy'.format(self.config['plant']), train_dataX)
        np.save('{}/fast_data/diff_Y.npy'.format(self.config['plant']), diff_Y)
        #  validation part:
        val_predict_Y = self.nn.implement(self.val_dataX)
        val_diff_Y = self.val_dataY - predict_Y
        #  remove overrange pair:
        overrange = np.argwhere(np.max(val_diff_Y, axis=1)>0.3)[:, 0]
        val_diff_Y = np.delete(val_diff_Y, overrange, axis=0)*3.0
        val_dataX = np.delete(self.val_dataX, overrange, axis=0)

        # down sample
        #  _, val_diff_Y = D.down_sample(val_diff_Y, 10, 1)
        #  _, val_dataX = D.down_sample(val_dataX, 10, 1)

        np.save('{}/fast_data/val_diff_X.npy'.format(self.config['plant']), val_dataX)
        np.save('{}/fast_data/val_diff_Y.npy'.format(self.config['plant']), val_diff_Y)
 
    def implement(self, iter_time=1):
        #  imdataX is the data come from target structure:
        #  imdatax should be (N, time_step, 9)
        im_dataX = scio.loadmat('matlab_id/data/im_data.mat'.format(self.config['plant']))['x']  #  experiemental scaled
        if len(im_dataX.shape) == 2:
            im_dataX = im_dataX[:, :, np.newaxis]

        for i in range(iter_time):
            d_im_dataX = D.x_process(im_dataX, self.config)
            predict_Y = self.nn.implement(d_im_dataX)
            predict_Y = predict_Y/self.config['scales'][-1]
            #  padd zero:
            z_num = predict_Y.shape[0]
            z_c = predict_Y.shape[-1]

            
            if self.config['diff'] == True:
                predict_Y = np.concatenate([np.zeros([z_num, 2+self.config['m'], z_c]), predict_Y,\
                np.zeros([z_num, 2, z_c])], axis=1)
                #  diff support iterations
            else:
                predict_Y = np.concatenate([np.zeros([z_num, self.config['m'], z_c]), predict_Y, np.zeros([z_num, num_diff, z_c])], axis=1)
                
            #  compensate zero
            num_diff = im_dataX.shape[1] - predict_Y.shape[1]
            predict_Y = np.concatenate([predict_Y, np.zeros([z_num, num_diff, z_c])], axis=1)

        #  reshape into standard shape
        scio.savemat('matlab_id/data/pre_data.mat'.format(self.config['plant']), {'yp':predict_Y})
        return predict_Y
