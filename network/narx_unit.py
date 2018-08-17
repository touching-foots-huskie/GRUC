import numpy as np
import tensorflow as tf

class Nu(tf.nn.rnn_cell.RNNCell):
    ''' A realization of WRNN '''
    def __init__(self, num_units, activation=tf.nn.tanh, reuse=None):
        super(Nu, self).__init__(_reuse=reuse)
        self._num_units = num_units
        self._activation = activation

    @property
    def state_size(self):
        return self._num_units

    @property
    def output_size(self):
        return self._num_units

    def call(self, input, state):
        # output in last time step is state in this timestep
        input = tf.concat([input, state], axis=-1)

        output = self.predict_model(input)
        return output, output

    def predict_model(self, layer):
        # ordinary networks
        net_dims = [32, 64, 32, 1]
        for dim in net_dims:
            layer = tf.layers.dense(layer, dim, activation=self._activation, kernel_initializer=tf.keras.initializers.Orthogonal())
        _output = layer
        return _output
