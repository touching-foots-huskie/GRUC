# : Harvey Chang
# : chnme40cs@gmail.com
# main function is used to make all configurations and making results:
import pdb
import argparse
import numpy as np
import tensorflow as tf
import dataset as D
from matplotlib import pyplot as plt
import train.trainer as trainer


def gen_config(args):
    config = dict()
    config['plant']= args.plant
    config['mode'] = args.mode
    config['network'] = args.network
    config['recurrent'] = args.recurrent
    config['continue'] = args.cont
    config['stack_num'] = args.stack
    # changing part:
    config['time_step'] = 1  # predict in segment
    config['c_step'] = 1 # continuous time step
    config['training_epochs'] = 600
    config['batch_size'] = 64 if config['plant'] == 'arc' else 128  # arc: 64| pid: 128
    config['learning_rate'] = 5e-3  
    # config['learning_rate'] = 5e-3  
    # arc: 64| pid: 128 # arc: 1e-3| pid: 1e-2
    config['scales'] = [10.0, 3.0e2, 4.0e4, 1.0e6, 8.0e4] 

    config['dim'] = 4*(config['c_step']*2+config['time_step']) 
    config['out_dim'] = config['time_step']
    
    config['diff'] = True  # if differentiate inside
    # params for signals:
    config['file_path'] = 'matlab_id/data/{}/sample'.format(config['plant']) 
    config['val_path'] = 'matlab_id/data/{}/sample'.format(config['plant']) 

    # log structure
    config['save'] = True
    if (config['mode'] == 'train' or config['mode'] == 'res_train') and (not config['continue']):
        config['restore'] = False
    else:
        config['restore'] = True

    # directory for tensorboard
    config['board_dir'] = 'train_log/log'

    # the name of saved model
    config['model_name'] = '{}_model_c{}_{}'.format(config['plant'], config['c_step'], config['network'])
    return config


def run(config):
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
    # fix config
    parser = argparse.ArgumentParser(description='config for plant & network & mode')
    parser.add_argument('-p', '--plant', default='pid', choices=['pid', 'arc'])
    parser.add_argument('-n', '--network', default='rnn', choices=['rnn', 'narx'])
    parser.add_argument('-m', '--mode', default='implement', choices=['train', 'validation', 'implement'])
    parser.add_argument('-c', '--cont', default=True, choices=[True, False])
    parser.add_argument('-r', '--recurrent', default=True, choices=[True, False])
    parser.add_argument('-s', '--stack', default=1)
    args = parser.parse_args()
    config = gen_config(args)
    run(config)
