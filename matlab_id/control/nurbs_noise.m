% add nurbs in nose level:
% ys= d3_gen(3, 20, 0.05);| reference parameter
function yo = nurbs_noise(yo, T, A)
%% gen ctrl points: 
% o_sig means orignal signal
N = 3;
Ts = 3;
fs = 5000;
% setting control points:
%% generating x0:
delta_max = random('unif', 0.5, 1.0);
delta_min = 0.15;
% xs = linspace(-5, 0.2, round(N));
xs = -1.0*ones(1, round(N));
xe = (T+1)*ones(1, round(N));
x0 = [];
x = 0;
while(x<T)
    x0 = [x0, x];
    deltax = abs(random('unif', delta_min, delta_max));
    x = x + deltax;
end
ys = zeros(1, round(N));
y0 = random('norm', 0, 0.5, 1, max(size(x0)))*A;

%%
% add p2p 
y0 = [ys, y0, ys];
x0 = [xs, x0, xe];
% scatter(x0+Ts, y0);
%% get knots
hold on;
% sp = spmak(knots,ctrlpoints); %生成B样条函数
sp = spapi(5,x0, y0); %生成B样条函数

%% sample points;
tm = -Ts:1/fs:T+Ts;    % time used in middle
ys = fnval(sp,tm)';

%% half copy structure:
% data has the same min ad:
% when T0 = 5, this = 20001
assert(min(find(ys)) == 10001, 'Not starting from the same point');
assert(max(abs(ys))<0.10, 'Over the range!');
% add to yo:非零部分相加
% ys的非零部分：
ad = find(ys);
% yo非零部分：
p = min(find(abs(yo-0.1)<1e-10));
oad = find(abs(yo(p:end)-0.1)>1e-10)+p;
leno = max(oad) - min(oad);
yo(min(oad):max(oad), :) = ys(min(ad):(min(ad)+leno), :)*0.1 + yo(min(oad):max(oad), :);
end