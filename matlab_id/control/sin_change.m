% add nurbs in nose level:
% ys= d3_gen(3, 20, 0.05);| reference parameter
function yo = sin_change(yo)
%% gen ctrl points: 
% o_sig means orignal signal
T = 20;
A = 0.03;
fs = 5000;
w = 2;
% setting control points:
%% generating x0:
T = round(T/(2*pi))*2*pi;
T0 = 10;  %wait time

%% get signal:
tm = [0:1/fs:T-1/fs]';
u = cos(w*tm)-1;
ys = [zeros(T0*fs, 1); u; zeros(T0*fs, 1)]*A/2;
%%

% add new noise with o_sig
ad = find(ys);
oad = find(yo);
% data has the same min ad:
% when T0 = 5, this = 20001
assert(min(find(ys)) == 50002, 'Not starting from the same point');
assert(max(abs(ys))<0.10, 'Over the range!');

yo(min(oad):max(oad), :) = ys(min(ad):max(ad), :);
end