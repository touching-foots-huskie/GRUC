% add nurbs in nose level:
function yo = nurbs_noise(yo, T, A)
N = 3;
Ts = 3;
fs = 5000;

delta_max = random('unif', 0.5, 1.0);
delta_min = 0.15;
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
y0 = [ys, y0, ys];
x0 = [xs, x0, xe];

hold on;
sp = spapi(5,x0, y0);

tm = -Ts:1/fs:T+Ts; 
ys = fnval(sp,tm)';

assert(min(find(ys)) == 10001, 'Not starting from the same point');
assert(max(abs(ys))<0.10, 'Over the range!');

ad = find(ys);
p = min(find(abs(yo-0.1)<1e-10));
oad = find(abs(yo(p:end)-0.1)>1e-10)+p;
leno = max(oad) - min(oad);
yo(min(oad):max(oad), :) = ys(min(ad):(min(ad)+leno), :)+yo(min(oad));
end
