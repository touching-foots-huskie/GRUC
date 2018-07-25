function sig = down_sample(sig, d_step)
ad = 1:d_step:(floor(size(sig,1)/d_step-1)*d_step+1);
sig = sig(ad, :);
end