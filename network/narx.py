# narx.py: narx version of prediction network

import pdb
import random
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt

class network:
    def __init__(self, config):
        self.config = config
        self.net_dims = [32, 64, 32, 1]

        self.output = self.build_net()
        # training structure:
        self.loss = tf.losses.mean_squared_error(self.output, self.label)
        self.opt = tf.train.AdamOptimizer(config['learning_rate'])
        self.train_op = self.opt.minimize(self.loss)
        self.sess = tf.Session()

        self.saver = tf.train.Saver(tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='dense'))
        # start a sess and initial it.
        self.sess.run(tf.initialize_variables(tf.global_variables()))
        
    def build_net(self):
        self.input = tf.placeholder(tf.float32, shape=(None, self.config['seg_len'], self.config['dim']+1)) # using (e, x, v, a, j)_(t-1) to predict e_t
        self.label = tf.placeholder(tf.float32, shape=(None, self.config['seg_len'], 1))

        _layer = self.input

        with tf.variable_scope('dense'):
            for _dim in self.net_dims:
                _layer = tf.layers.dense(_layer, _dim, kernel_initializer= tf.keras.initializers.Orthogonal())
        return _layer

    def save(self):
        self.saver.save(self.sess, 'train_log/narx_model')
        
    def restore(self):
        self.saver.restore(self.sess, 'train_log/narx_model')

    def train(self, x, y):
        for epoch, data_dict in zip(range(self.config['training_epochs']), self.data_dict_gen(x, y)):
            _, loss = self.sess.run([self.train_op, self.loss], feed_dict=data_dict)  
            print("epoch:{}|loss:{}".format(epoch, loss))

        print("training finished!")

    # generating data_dicts:
    # x[t-1], e[t-1], y[t]
    def validate(self, x, y):
        output = self.predict(x, y)
        print("validation finished!")
        for i in range(x.shape[0]):
            plt.plot(output[i].ravel(), label='prediction')
            plt.plot(y[i].ravel(), label='actual')
            plt.legend()
            plt.show()

    def predict(self, x, y):
        # process data
        data_x = np.concatenate([x[:, 1:], y[:,:-1]], axis=-1)
        output = self.sess.run(self.output, feed_dict={self.input:data_x})
        return output

    def data_dict_gen(self, x, y):
        '''
        x: (None, seg_len, 4)
        y: (None, seg_len, 1)
        '''
        x = np.concatenate([x[:, 1:], y[:,:-1]], axis=-1)
        y = y[:, 1:]
        while True:
            num = np.random.randint(low=1, high=x.shape[0], size=self.config['batch_size'])
            data_dict = dict()
            data_dict[self.input] = x[num]
            data_dict[self.label] = y[num]
            yield data_dict
