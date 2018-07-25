# Data description
## PID data
### data for train
+ 21-30 pid in 40 seconds I.
+ 31-40 ilc version of above.

+ 46-55: pid in 40 seconds II.
+ pid_train/41-50 ilc of above. 

### data for test
+ 41-45 control& prediction test| 60 run on prediction
> 44: best ILC, 41: PID, 42: first ILC, 43: GRU (1st), 45: GRU (2 nd), 60: best GRU
   

+ 61-63 sin prediction 
> 61 sin signal first PID, 62 sin signal first ILC, 63 sin signal second ILC.

+ 56-59: XY cognate test.
