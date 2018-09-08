function sig = nurbs_gen(N, T, A)
%% gen ctrl points: 
Ts = 3;
fs = 5000;
% setting control points:
%% generating x0:
flag = 1;
while flag
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
    % sp = spmak(knots,ctrlpoints); 
    sp = spapi(5,x0, y0); 

    %% sample points;
    tm = -Ts:1/fs:T+Ts;    % time used in middle
    ys = fnval(sp,tm);

    %% half copy structure:
    % data has the same min ad:
    % when T0 = 5, this = 20001
    try
        assert(min(find(ys)) == 10001, 'Not starting from the same point');
        assert(max(abs(ys))<0.10, 'Over the range!');
        flag = 0; % finish part
    catch
        flag = 1; % regenerate
        disp('try again');
    end
end
% add p2p trajectory:
load('p.mat');
Tz = 5;
ys = [zeros(1, 5000*Tz), p', ys+p(end)];
tu = 0:1/fs:T+2*Ts+1.4+Tz;
plot(tu, ys);
% DrawFFT(ys, 5000);
sig = [tu', ys'];
end
