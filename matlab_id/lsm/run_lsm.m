clc
clear 

%% learn from a specific data part
addpath ../tool
No = 30;

No2 = 44; % examed data
fs = 5000;
mode = 'pid';
file_path = '../measure/log/mat/pid';

% load data
load(sprintf( '%s/%d.mat', file_path, No)); 
c = rec.Y(1).Data';
x = rec.Y(4).Data';
y = rec.Y(3).Data';

% exam data
load(sprintf( '%s/%d.mat', file_path, No2));
c2 = rec.Y(1).Data';
x2 = rec.Y(4).Data';
y2 = rec.Y(3).Data';

e = noise_filt(x - y) + c;
e2 = noise_filt(x2 - y2) + c2;

% the best compensation
p = min(find(abs(x-0.1)<1e-5));
ad = find(abs(x(p:end)-0.1)>1e-5)+p;
start_p = min(ad);
end_p = max(ad);

%% clip data:
x = x(start_p:end_p);
y = y(start_p:end_p);
e = e(start_p:end_p);

% differentiate of x
v = (x(1:end-1) - x(2:end))*fs;
a = (v(1:end-1) - v(2:end))*fs;

% pad zero on:
v = [v; 0];
a = [a; 0; 0];

% exam x, v, a
p2 = min(find(abs(x2-0.1)<1e-5));
ad2 = find(abs(x(p2:end)-0.1)>1e-5) + p2;
start_p = min(ad2);
end_p = max(ad2);

x2 = x2(start_p:end_p);
e2 = e2(start_p:end_p);

v2 = (x2(1:end-1) - x2(2:end))*fs;
a2 = (v2(1:end-1) - v2(2:end))*fs;

v2 = [v2; 0];
a2 = [a2; 0; 0];

% start lqr:
A = [x, v, a];

A2 = [x2, v2, a2];
T = A'*A;
theta = (T)\A'*e;

% make prediction on e2
ep = A2 * theta;
t = 1/fs:1/fs:max(size(ep))/fs;
plot(t, e2);
hold on
plot(t, ep);

% statistic value of error
rms(e2 - ep)
max(e2 - ep)

legend('experiment', 'prediction');
xlabel('time (s)');
ylabel('tracking error (m)');
