# : Harvey Chang
# : chnme40cs@gmail.com
# main function is used to make all configurations and making results:
import tqdm
import numpy as np
import tensorflow as tf
import dataset as D
from matplotlib import pyplot as plt
import train.trainer as trainer


def main():
    config = dict()
    #  mode
    config['plant'] = 'pid'
    config['mode'] = 'train'
    config['continue'] = False

    #  changing part:
    config['time_step'] = 1  # predict in segment
    config['training_epochs'] = 400
    config['batch_size'] = 64 if config['plant'] == 'arc' else 128  # arc: 64| pid: 128
    config['learning_rate'] = 1e-3 if config['plant'] == 'arc' else 1e-2  
    # arc: 64| pid: 128 # arc: 1e-3| pid: 1e-2
    config['scales'] = [10.0, 5e2, 8e4, 2e6, 8e4] 

    config['m'] = 1  # previous m x and y
    config['dim'] = 4*(config['m']*2+config['time_step'])
    config['out_dim'] = config['time_step']
    
    config['diff'] = True  # if differentiate inside
    #  params for signals:
    config['file_path'] = '{}/data/data'.format(config['plant']) 
    config['val_path'] = '{}/data/data'.format(config['plant']) 

    #  log structure
    config['save'] = True
    if (config['mode'] == 'train' or config['mode'] == 'res_train') and (not config['continue']):
        config['restore'] = False
    else:
        config['restore'] = True

    #  directory for tensorboard
    config['board_dir'] = 'train_log/log'

    #  read datas:
    mode = config['mode']
    if mode == 'res_train' or mode == 'res_test':
        dataX, dataY, val_dataX, val_dataY = gen_data()

    else:
        dataX, dataY = D.read_data(config['file_path'], config)
        val_dataX, val_dataY = D.read_data(config['val_path'], config)  # when no test: is data/data

    mytrainer = trainer.Trainer(config)
    #  add data:
    if mode == 'res_train' or mode == 'res_test':
        mytrainer.add_raw(dataX, dataY)
        mytrainer.add_raw(val_dataX, val_dataY, data_type='validation')
    else:
        mytrainer.add_data(dataX, dataY)
        mytrainer.add_data(val_dataX, val_dataY, data_type='validation')

    if config['mode'] == 'train' or config['mode'] == 'res_train':
        mytrainer.train()
    elif config['mode'] == 'test' or config['mode'] == 'res_test':
        mytrainer.test()
    elif config['mode'] == 'implement':
        mytrainer.implement()
    elif config['mode'] == 'gendiff':
        mytrainer.gendiff()

# data come from:
def gen_data():
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


if __name__ == '__main__':
    main()
