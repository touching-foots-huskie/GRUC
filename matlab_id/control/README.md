# Important functions
+ exam predict.m
> exam the prediction of the network| usage: put the pre.mat into ../train and run this file.
+ exam result.m
> compare different control method
+ imgen.m
> generate implemention data based on one reference.
+ nurbs noise/sin noise.m
> add noise to previous data| used in Set2 of ILC.
+ nurbs change/sin change.m
> change reference into another signal with equal length| used in Set3 of ILC.

## Example of prediction comparation
### NURBS
+ im_gen(false, 44, 1)
+ im_gen(false, 44, 2)
+ im_gen(false, 44, 3)

### SIN
+ im_gen(false, 63, 4)
+ im_gen(false, 63, 5)
+ im_gen(false, 63, 6)
