# narx.py: narx version of prediction network

import random
import numpy as np
import tensorflow as tf

class network:
    def __init__(self, config):
        self.config = config
        self.net_dims = [32, 64, 32, 1]

        self.output = self.build_net()
        # training structure:
        self.loss = tf.losses.mean_squared_error(self.output - self.label)
        self.opt = tf.train.AdamOptimizer(config['learning_rate'])
        self.train_op = self.opt.minimize(self.loss)
        self.saver = tf.trainer.Saver(tf.Graph.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES), scope='dense')
        # start a sess and initial it.
        self.sess = tf.Session()
        self.sess.run(tf.initialize_variables(tf.global_variables())
        
    def build_net(self):
        self.input = tf.placeholder(tf.float32, shape=(None, self.config['time_steps'], self.config['dim']+1)) # using (e, x, v, a, j)_(t-1) to predict e_t
        self.label = tf.placeholder(tf.float32, shape=(None, self.config['time_steps'], 1))

        _layer = self.input

        with tf.variable_scope('dense'):
            for _dim in self.net_dims:
                _layer = tf.layers.dense(_layer, _dim, kernel_initializer= tf.keras.initializers.Orthogonal())
        return _layer

    def save(self):
        self.saver.save(self.sess, 'train_log/narx_model')
        
    def restore(self):
        self.saver.restore('train_log/narx_model')

    def train(self, x, y):

        # restore/ 
        if self.config['restore']:
            self.restore()
        for epoch, data_dict in self.config['epochs'], self.data_dict_gen(x, y):
            _, loss = self.sess.run(self.train_op, self.loss, feed_dict = data_dict)  
            print("epoch:{}|loss:{}".format(epoch, loss))

        print("training finished!")
        if self.config['save']:
            self.save()

    # generating data_dicts:
    # x[t-1], e[t-1], y[t]

    def data_dict_gen(self, x, y):
        '''
        x: (None, time_s, 4)
        y: (None, time_s, 1)
        '''
        x = np.concatenate([x[:, 1:], y[:,:-1]], axis=-1)
        y = y[:, 1:]
        assert x.shape == y.shape
        while True:
            num = random.randint(self.config['batch_size'])
            data_dict = dict()
            data_dict[self.input] = x[num]
            data_dict[self.label] = y[num]
            yield data_dict
