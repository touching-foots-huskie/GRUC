% run: generating training sets:
clc
clear
%
addpath ../tool
%% 1. read data:
mode = 'pid'
Start = 31;
End = 50;
filenames = cell((End-Start+1), 1);
file_dir = '../measure/log/mat/pid_train';

for i=1:1:(End-Start+1)
% filenames(i) = {sprintf('../measure/log/mat/exam/%d.mat', i+Start-1)};
filenames(i) = {sprintf('%s/%d.mat', file_dir, i+Start-1)};
end

% neccessary datas:
% get seq len:
filename = char(filenames(1));
[xp, eall, fs] = read_data(filename);
seqlen = size(xp,1);
% config
batchlen = 10000;
filenum = size(filenames, 1);

% Ed = zeros(filenum, seqlen, 1);

%% 2. process data
% notice: state has been processed in matlab
% make it fit in different size:
X = [];
E = [];
for i = 1:1:filenum
    filename = char(filenames(i));
    [xp, eall, fs] = read_data(filename);
    % resize here| concat:
    secnum = floor(size(xp, 1)/batchlen);
    x = reshape(xp(1:secnum*batchlen), batchlen, secnum); 
    e = reshape(eall(1:secnum*batchlen), batchlen, secnum); 
    % error process| filt bad segment:
    threshold = 2e-5;
    if(abs(max(max(e)))>threshold)
        % find part that can be used:
        ft = (max(e)<threshold);
        x = x(:, ft);
        e = e(:, ft);
    end
    X = [X, x];
    E = [E, e];
end

%% 3. save: clip and downsample:
% change into x and y
x = X;  % minus bias
y = E;
% yb = Ed;
x = down_sample(x, 10);
y = down_sample(y, 10);

% shape:
x = x';
y = y';

save(sprintf('../data/%s/sample/x.mat', mode),'x');
save(sprintf('../data/%s/sample/y.mat',mode),'y');
% save('../data/yb.mat', 'yb');
