# : Harvey Chang
# : chnme40cs@gmail.com
# main function is used to make all configurations and making results:
import numpy as np
import tensorflow as tf
import dataset as D
from matplotlib import pyplot as plt
import train.trainer as trainer


def main():
    config = dict()
    #  mode
    config['plant'] = 'pid'
    config['mode'] = 'implement'
    config['continue'] = False

    #  changing part:
    config['time_step'] = 1  # predict in segment
    config['training_epochs'] = 600
    config['batch_size'] = 64 if config['plant'] == 'arc' else 128  # arc: 64| pid: 128
    config['learning_rate'] = 5e-3  
    # arc: 64| pid: 128 # arc: 1e-3| pid: 1e-2
    config['scales'] = [10.0, 3e2, 4e4, 1e6, 8e4] 

    config['dim'] = 4
    config['out_dim'] = 1
    
    config['diff'] = True  # if differentiate inside
    #  params for signals:
    config['file_path'] = 'matlab_id/data/{}/sample'.format(config['plant']) 
    config['val_path'] = 'matlab_id/data/{}/sample'.format(config['plant']) 

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
    dataX, dataY = D.read_data(config['file_path'], config)

    mytrainer = trainer.Trainer(config)
    mytrainer.add_data(dataX, dataY)

    if config['mode'] == 'train':
        mytrainer.train()
    elif config['mode'] == 'test':
        mytrainer.test()
    elif config['mode'] == 'implement':
        mytrainer.implement()


if __name__ == '__main__':
    main()
