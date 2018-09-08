function im_gen(raw, inNum, stackout) 
% generate prediction data for new/old traj
% if raw is true, gen forward, else gen reverse.
addpath ../tool
if raw
    load(sprintf('../measure/signal/stack%d/sig.mat', inNum));
    x0 = sig(:, 2);
else
    file_path = '../measure/log/mat/pid';
    % read data:
    load(sprintf('%s/%d.mat',file_path, inNum));   
    x0 = rec.Y(4).Data';
    % test for target:
    y0 = rec.Y(3).Data';
    c0 = rec.Y(1).Data';
    e0 = noise_filt(x0-y0)+c0;
end
xr = x0; % raw x0;
% add zero infront of the signal:
x0 = down_sample(x0, 10);

% cut down
p0 = min(find(abs(x0-0.1)<1e-10));
x = x0(p0:end)-0.1;
x = x';

save(sprintf('../data/prediction/stack%d/raw_data.mat', stackout), 'xr');
save(sprintf('../data/prediction/stack%d/im_data.mat', stackout), 'x');

if ~raw
    % process e:
    e0 = down_sample(e0, 10);
    e = e0(p0:end);
    e = e';
    save(sprintf('../data/prediction/stack%d/data.mat', stackout), 'rec');
    save(sprintf('../data/prediction/stack%d/t_error.mat', stackout), 'e');
end
