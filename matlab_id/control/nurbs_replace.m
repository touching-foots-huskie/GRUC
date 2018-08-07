% add nurbs in nose level:
function [yo, ocomp] = nurbs_replace(yo, Num, file_path)
% load Num
load(sprintf( '%s/%d.mat',file_path, Num));    
c1 = rec.Y(1).Data';
x1 = rec.Y(4).Data';
y1 = rec.Y(3).Data';
% For ILC:
% filt uncontrol noise:| ILC compensation
c = noise_filt(x1 - y1);
comp = c1+c;

% replace
pin = min(find(abs(x1-0.1)<1e-5));
inad = find(abs(x1(pin:end)-0.1)>1e-5)+pin;
lenin = max(inad) - min(inad);

% cut for o
p = min(find(abs(yo-0.1)<1e-5));
oad = find(abs(yo(p:end)-0.1)>1e-5)+p;
leno = max(oad) - min(oad);

lenu = min(leno, lenin);
yo(min(oad):min(oad)+lenu, :) = x1(min(inad):(min(inad)+lenu), :) + yo(min(oad)) - x1(min(inad));

ocomp = zeros(max(size(yo)), 1);
ocomp(min(oad):min(oad)+lenu, :) = comp(min(inad):(min(inad)+lenu), :);

end
