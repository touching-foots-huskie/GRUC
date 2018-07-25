% exam results:
clc
clear 
number = [41, 41, 41];
names = [{'PID'}, {'ILC'}, {'GRUC'}];
color = [{'b'}, {'r'}, {'g'}];
file_path = '../measure/log/mat/pid';
%% first time:
for i = 1:1:max(size(number))
    load(sprintf('%s/%d.mat', file_path, number(i)));
    c = rec.Y(1).Data';
    x = rec.Y(4).Data';
    y = rec.Y(3).Data';

    t = (0:1/5000:(size(x)/5000-1/5000))';
    e = x - y;
    e = noise_filt(e);

    % alignment
    p = min(find(abs(x-0.1)<1e-10));
    ad = find(abs(x(p:end)-0.1)>1e-10)+p;
    start_p = min(ad);
    if i == 1
        pad = floor(start_p*0.05);
        end_p = max(ad);
    else
        end_p = min(start_p+pad+size(t,1), max(size(e)));
    end
    start_p = start_p + pad;

    subplot(max(size(number)),1,i);
    plot(t(1:end_p-start_p + 1), e(start_p:end_p), sprintf('%s', char(color(i))));
    if i == 1
        axis([10, 20, -1e-5, 1e-5]);
    else
        axis([10, 20, -1e-5, 1e-5]);
    end
    ylabel(sprintf('%s (m)', char(names(i))));
    rms(e(start_p+pad:end_p))
    max(e(start_p+pad:end_p))
end

