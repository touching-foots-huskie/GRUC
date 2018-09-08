function exam_prediction(num1, num2, num3, fname)
% this script is used to make comparation between predictions
addpath  ../tool
number = [num1, num2, num3];
names = [{'LSM'}, {'NARX'}, {'GRU'}];
color = [{'b'}, {'r'}, {'m'}];
file_path = '../data/prediction';
%% first time:
error_list = zeros(max(size(number)), 2);
for i = 1:1:max(size(number))

    load(sprintf('%s/stack%d/data.mat', file_path, number(i)))
    load(sprintf('%s/stack%d/pre_data.mat', file_path, number(i)))

    % process data:
    c1 = rec.Y(1).Data';
    x1 = rec.Y(4).Data';
    y1 = rec.Y(3).Data';

    e = noise_filt(x1 - y1) + c1;
    % the best compensation
    p1 = min(find(abs(x1-0.1)<1e-10));
    ad = find(abs(x1(p1:end)-0.1)>1e-10) + p1;
    start_p = min(ad);
    end_p = min(max(ad), max(size(e)));
    ce = e(start_p:end_p);

    % get t:
    t = 0:1/5000:(size(ce)/5000-1/5000);

    % get p0:
    x0 = down_sample(x1, 10);
    p0 = min(find(abs(x0-0.1)<1e-10));

    % reshape yp:
    yp = reshape(yp, [1, max(size(yp))]);
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

    % plot figures
    subplot(max(size(number)),1,i);
    plot(t, ce, 'k');
    hold on
    plot(t, ccomp, sprintf('%s', char(color(i))));
    if i == 1
        axis([10, 20, -1e-5, 1e-5]);
    else
        axis([10, 20, -1e-5, 1e-5]);
    end
    ylabel(sprintf('%s (m)', char(names(i))));
    pre_error = ce - ccomp;
    error_list(1, i) = rms(pre_error)*1e6;
    error_list(2, i) = max(pre_error)*1e6;
end

% save figure
% saveas(gcf, sprintf('figures/%s', fname), 'eps');

% save data
fid = fopen(sprintf('%s.txt', fname), 'w');
for j = 1:1:2
    fprintf(fid, '%3f & %3f & %3f\n', error_list(j, 1), error_list(j, 2), error_list(j, 3));
end
fclose(fid);

