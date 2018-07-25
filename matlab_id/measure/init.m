% all init:
% for pid structure:
clc
clear
% add path:
addpath ../tool
addpath signal
% init
pid
% arc
% d1 parameter
% FC: forward compensation| GN: generate nurbs| GS: generate sin
% LD: load data
mode = 'GS'; 
N = 3; % ��Ե�⻬�״�
T = 40;  % ����ʱ��|  110 for train and 10 for test:
T_sim = T;  % T_sim is the configuration for simulink
A = 0.03; % ���з�ֵ
fs = 5000;

if(strcmp(mode, 'GN'))
    %d1 gen: NRUBS 
    sig = nurbs_gen(N, T, A);
    % zero compensate:
    compensate = [sig(:,1), zeros(size(sig(:,1), 1),1)];
    save('signal/sig.mat', 'sig');
    
elseif(strcmp(mode, 'GS'))
    w = 3; % �����ź�Ƶ��
    sig = sin_gen(w, fs, T, A);
    compensate = [sig(:,1), zeros(size(sig(:,1), 1),1)];
    save('signal/sig.mat', 'sig');
    
elseif(strcmp(mode, 'FC'))
    % ILC ����| ���粹������
    load('signal/sig.mat');
    load('signal/compensate.mat');
    hold on
    plot(sig(:, 2));

elseif(strcmp(mode, 'LD'))
    load('sig.mat');
    x1 = sig(:, 2);
    t = 0:1/5000:(size(x1)/5000-1/5000);
    sig = [t', x1];
    compensate = [sig(:,1), zeros(size(sig(:,1), 1),1)];
    plot(t', x1);
else
    error('No such mode.');
end
