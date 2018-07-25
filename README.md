# Proposal
This program is used to identify and predict the motion of a linear motor. The proposed control method is called GRUC.
# Structure
+ network/rnn.py
> construct network
+ train/trainer.py
> train network
+ dataset.py
> generate dataset
+ main.py
> give configuration
+ hyper param.py
> find best parameters
## dataset.py
+ read mat
> read from mat
+ read data
> read from file
+ xy process
> used in trainer.py| add data()
+ x process
> used in network/rnn.py | implement
+ down sample
