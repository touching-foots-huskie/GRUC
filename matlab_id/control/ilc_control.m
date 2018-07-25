% ilc control and noised ilc control
clc
clear 
No = 44; % original PID or ILC in previous iter
file_path = '../measure/log/mat/pid';

% noise
noise = false;
change = true;

% parameters:
T = 40; 
T_sim = T; 
A = 0.03;

load(sprintf( '%s/%d.mat',file_path, No));    
c1 = rec.Y(1).Data';
x1 = rec.Y(4).Data';
y1 = rec.Y(3).Data';
% For ILC:
% filt uncontrol noise:| ILC compensation
c = noise_filt(x1 - y1);
comp = c1+c;
hold on

% add zero infront of the signal:
Ts = 5;
fs = 5000;
x1 = [zeros(Ts*fs, 1); x1];
t = 0:1/5000:(size(x1)/5000-1/5000);
%% Nurbs noise
if noise
    plot(t', x1);
    hold on
    x1 = nurbs_noise(x1, T, A);
    plot(t', x1);
end

%% Total different curves:
if change
    plot(t', x1);
    hold on
    x1 = nurbs_change(x1, T, A);
    plot(t', x1);
end
%% Concat Structure
sig = [t', x1];
comp = [zeros(Ts*fs, 1); comp];
compensate = [t', comp];

%% Save the data:
save('../measure/signal/sig.mat', 'sig');
save('../measure/signal/compensate.mat', 'compensate');
