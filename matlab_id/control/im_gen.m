% this script is going to produce prediction on some mat:
clc
clear
addpath ../tool
No = 44;
file_path = '../measure/log/mat/perfect';

% read data:
load(sprintf('%s/%d.mat',file_path, No));   
c0 = rec.Y(1).Data';
x0 = rec.Y(4).Data';
y0 = rec.Y(3).Data';
% add zero infront of the signal:
x0 = down_sample(x0, 10);
% cut down
p0 = min(find(abs(x0-0.1)<1e-10));
x = x0(p0:end)-0.1;
x = x';
save('../data/im_data.mat', 'x');
save('p0.mat', 'p0');
