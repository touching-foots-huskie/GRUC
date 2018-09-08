import os
import matlab
import matlab.engine

mode_num = 1
mode_list = ['prediction comparation', 'batch prediction']
mode = mode_list[mode_num]
eng = matlab.engine.start_matlab()
print('engine start')
if mode == 'prediction comparation':
    # generate im_data:
    print('im_data generating')
    eng.cd('matlab_id/control')
    eng.im_gen(0, 44, 1, nargout=0)
    eng.im_gen(0, 44, 2, nargout=0)
    eng.im_gen(0, 44, 3, nargout=0)
    eng.im_gen(0, 63, 4, nargout=0)
    eng.im_gen(0, 63, 5, nargout=0)
    eng.im_gen(0, 63, 6, nargout=0)
    print('generation finished')
    # make prediction
    # lsm:
    print('starting prediction')
    eng.run_lsm(1, nargout=0)
    eng.run_lsm(4, nargout=0)
    # run narx
    for _name, _stack in zip(['narx', 'narx', 'rnn', 'rnn'], [2, 4, 3, 6]):
        try:
            os.system('python main.py -n {} -s {}'.format(_name, _stack))
        except:
            pass
        else:
            print('finished {} {}'.format(_name, _stack))
    # make examination 
    eng.exam_prediction(1, 2, 3, 'P_C1', nargout=0)
    eng.exam_prediction(4, 5, 6, 'P_C2', nargout=0)
elif mode == 'batch prediction':
    # make noised and change traj
    eng.cd('matlab_id/control')
    print('start generating')
    eng.ilc_control('sin', 76, 2, 1, 0, nargout=0) # noised
    eng.ilc_control('sin', 76, 3, 0, 1, nargout=0) # changed

    print('finish generating')
    # im_gen
    eng.im_gen(1, 2, 2, nargout=0)  # noised
    eng.im_gen(1, 3, 3, nargout=0)  # changed

    print('start predicting')
    for _name, _stack in zip(['rnn', 'rnn'], [2, 3]):
        try:
            os.system('python main.py -n {} -s {}'.format(_name, _stack))
        except:
            pdb.set_trace()
        else:
            print('finished {} {}'.format(_name, _stack))
    print('finished prediction')
    eng.fpredict(2, 4, nargout=0)
    eng.fpredict(3, 5, nargout=0)
    print('finish implementation')

eng.quit()
