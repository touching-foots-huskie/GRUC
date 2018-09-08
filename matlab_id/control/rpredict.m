function rpredict(No1, stack_num)
% prediction for existing reference
addpath ../tool
file_path = '../measure/log/mat/pid';

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
% get p0:
x0 = down_sample(x1, 10);
p0 = min(find(abs(x0-0.1)<1e-10));
load('../data/pre_data.mat');
yp = [zeros(p0-1, 1);yp'];
yp = extend_sample(yp, 10);

% new predict is new compensate:
clen = min(size(c1, 1), size(yp, 1));
c1(1:clen) = yp(1:clen);
comp = c1;
% filt
comp(1:start_p) = 0;
comp(end_p:end)=0;
ccomp = comp(start_p:end_p);
hold on
plot(t, ccomp);
hold on
% error
% plot(ccomp - ce(1:size(ccomp,1)));
axis([10, 14, -1.2e-5, 1.2e-5]);
ylabel('Error (m)');
xlabel('Time (s)');
legend('experimental', 'prediction');
%% save the new compensation structure:
%% add T0 ahead of x1 and comp:
xs = zeros(5000*5, 1);
x1 = [xs;x1];
comp = [xs; comp];
tn = 0:1/5000:(size(x1)/5000-1/5000);
sig = [tn', x1];
compensate = [tn', comp];
%% save the data:
save(sprintf('../measure/signal/stack%d/sig.mat', stack_num), 'sig');
save(sprintf('../measure/signal/stack%d/compensate.mat', stack_num), 'compensate');
end
