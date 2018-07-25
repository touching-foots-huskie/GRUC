function sig = sin_gen(w, fs, T, A)
%  second generator of data:
%  we can use this structure to exam the previous data:
% here is the multi-sin structure.
T = round(T/(2*pi))*2*pi;

%% get signal:
tm = [0:1/fs:T-1/fs]';
x = A*(cos(w*tm)-1);

% add more:
load('p.mat');
Tz = 5;
x = [zeros(5000*Tz, 1); p; x+p(end)];
t = [0:1/fs:size(x, 1)/fs-1/fs]';
sig = [t, x];
plot(t, x);
end
