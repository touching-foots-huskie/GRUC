function im_gen(raw, stacknum, Num) 
% if raw is true, gen forward, else gen reverse.
addpath ../tool
if raw
    load(sprintf('../measure/signal/stack%d/sig.mat', stacknum));
    x0 = sig(:, 2);
else
    file_path = '../measure/log/mat/pid';
    % read data:
    load(sprintf('%s/%d.mat',file_path, Num));   
    x0 = rec.Y(4).Data';
end
% add zero infront of the signal:
x0 = down_sample(x0, 10);
% cut down
p0 = min(find(abs(x0-0.1)<1e-10));
x = x0(p0:end)-0.1;
x = x';
save('../data/im_data.mat', 'x');
save('p0.mat', 'p0');
end
