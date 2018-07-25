function [x, e, fs] = read_data(filename)
%% read data:
load(filename);
% new read data:
c = rec.Y(1).Data';
x = rec.Y(4).Data';
y = rec.Y(3).Data';
clip_ratio = 0.05;
t = rec.X.Data';
fs = round(1/(1000*(t(end) - t(end-1))))*1000;
% In NRUBS
% clip
p = min(find(abs(x-0.1)<1e-10));
ad = find(abs(x(p:end)-0.1)>1e-10)+p;

x = x(min(ad):max(ad),:)-0.1;
y = y(min(ad):max(ad), :)-0.1;
c = c(min(ad):max(ad), :);
e = (x - y);
e = noise_filt(e) + c; % ilc mode

% cut down after filt:
clip_step = floor(size(x, 1)*clip_ratio);
x = x(clip_step:end-clip_step, :);
e = e(clip_step:end-clip_step, :);
hold on
end
