function fpredict(stack_num_in, stack_num_out) 
addpath ../tool
load(sprintf('../measure/signal/stack%d/sig.mat', stack_num_in));
x = sig(:, 2);
% get p0:
x0 = down_sample(x, 10);
p0 = min(find(abs(x0-0.1)<1e-10));
load('../data/pre_data.mat');
yp = [zeros(p0-1, 1);yp'];
yp = extend_sample(yp, 10);
xs = zeros(5000*5, 1);
x1 = [xs; x];

% comp
c = zeros(max(size(x)), 1);
clen = min(max(size(yp)), max(size(c)));
c(1:clen) = yp(1:clen);
comp = c;
comp = [xs; comp];
tn = 0:1/5000:(size(x1)/5000-1/5000);
sig = [tn', x1];
compensate = [tn', comp];
%% save the data:
save(sprintf('../measure/signal/stack%d/sig.mat', stack_num_out), 'sig');
save(sprintf('../measure/signal/stack%d/compensate.mat', stack_num_out), 'compensate');
end
