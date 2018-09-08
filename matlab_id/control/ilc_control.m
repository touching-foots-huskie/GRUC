% ilc control and noised ilc control
function ilc_control(dtype, No, stack_num, noise, change)
addpath ../tool
file_path = '../measure/log/mat/pid';
% noise
replace = false;  % replace it with another traj
% if replace
Num = 44;

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
comp = [zeros(Ts*fs, 1); comp];
t = 0:1/5000:(size(x1)/5000-1/5000);
%% Nurbs noise
if noise
    plot(t', x1);
    hold on
    if strcmp(dtype, 'nurbs')
    	x1 = nurbs_noise(x1, T, A);
    elseif strcmp(dtype, 'sin')
        x1 = sin_noise(x1, T, A);
    end
    plot(t', x1);
end

%% Total different curves:
if change
    plot(t', x1);
    hold on
    if strcmp(dtype, 'nurbs')
        x1 = nurbs_change(x1, T, A);
    elseif strcmp(dtype, 'sin')
        x1 = sin_change(x1, T, A);
    end
    plot(t', x1);
end

%% Replace it with Num:
if replace
    plot(t', x1);
    hold on
    [x1, comp] = nurbs_replace(x1, Num, file_path);
    plot(t', x1);
end

%% Concat Structure
sig = [t', x1];
compensate = [t', comp];

%% Save the data:
save(sprintf('../measure/signal/stack%d/sig.mat', stack_num), 'sig');
save(sprintf('../measure/signal/stack%d/compensate.mat', stack_num), 'compensate');
