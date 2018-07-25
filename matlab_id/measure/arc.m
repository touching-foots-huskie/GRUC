% ARC experiment initialization
% signal parameters
Ts = 0.0002;
Amp = 0.05;
Freq = 1*2*pi;
Bias = Amp;
Phase = -pi/2;

vel = 0.005;
% input = timeseries;
T_pre = 10;

% controller parameters
M_hat0 = 0.18;
B_hat0 = 1.14;
Af_hat0 = 0.37;
dn_hat0 = 0;

gamma_M = 10;
gamma_B = 10;
gamma_Af = 1;
gamma_dn = 8000;
lambda = 300; % Kp

% robust
ks = 100; % robust
epsilon = 0.8;
delta = 0.01;

% Hardware
x0_abs = 0;
y0_abs = 0;

