% add nurbs in nose level:
% ys= d3_gen(3, 20, 0.05);| reference parameter
function yo = sin_noise(yo, T, A)
%% gen ctrl points: 
% o_sig means orignal signal
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
% data has the same min ad:
% when T0 = 5, this = 20001
assert(min(find(ys)) == 50002, 'Not starting from the same point');
assert(max(abs(ys))<0.10, 'Over the range!');

ad = find(ys);
p = min(find(abs(yo-0.1)<1e-10));
oad = find(abs(yo(p:end)-0.1)>1e-10)+p;

upper = min(max(oad), max(size(yo)));
leno = upper - min(oad);

yo(min(oad):upper, :) = ys(min(ad):(min(ad)+leno), :)*0.1 + yo(min(oad):upper, :);
end