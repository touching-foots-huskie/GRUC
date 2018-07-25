% exam prediction:
% add the prediction structure into exam:
%% load the data we want to exam:
clc
clear 

addpath ../tool
No1 = 44;
No2 = 44;
file_path = '../measure/log/mat/perfect';

%% plot yo:
load(sprintf( '%s/%d.mat',file_path, No1)); 
c1 = rec.Y(1).Data';
x1 = rec.Y(4).Data';
y1 = rec.Y(3).Data';

e = noise_filt(x1 - y1)+c1;
% the best compensation
p1 = min(find(abs(x1-0.1)<1e-10));
ad = find(abs(x1(p1:end)-0.1)>1e-10)+p1;
start_p = min(ad);
end_p = max(ad);
ce = e(start_p:end_p);

% get t:
t = 0:1/5000:(size(ce)/5000-1/5000);

plot(t, ce);

%% process yp:
hold on
load(sprintf( '%s/%d.mat',file_path, No2));
c2 = rec.Y(1).Data';
x2 = rec.Y(4).Data';
y2 = rec.Y(3).Data';

% get p0:
x0 = down_sample(x2, 10);
p0 = min(find(abs(x0-0.1)<1e-10));
load('../data/pre_data.mat');
yp = [zeros(p0-1, 1);yp'];
yp = extend_sample(yp, 10);

% new predict is new compensate:
c1(1:size(yp, 1)) = yp;
comp = c1;
% filt
p2 = min(find(abs(x2-0.1)<1e-10));
ad = find(abs(x2(p2:end)-0.1)>1e-10)+p2;
start_p = min(ad);
end_p = max(ad);
comp(1:start_p) = 0;
comp(end_p:end)=0;
ccomp = comp(start_p:end_p);
hold on
plot(t, ccomp);
hold on
% error
% plot(ccomp - ce(1:size(ccomp,1)));
axis([10, 14, -1.2e-5, 1.2e-5]);
ylabel('PID Error (m)');
xlabel('Time (s)');
legend;
%% save the new compensation structure:
%% add T0 ahead of x1 and comp:
xs = zeros(5000*5, 1);
x1 = [xs;x1];
comp = [xs; comp];
t = 0:1/5000:(size(x1)/5000-1/5000);
sig = [t', x1];
compensate = [t', comp];
%% save the data:
save('../measure/signal/sig.mat', 'sig');
save('../measure/signal/compensate.mat', 'compensate');
