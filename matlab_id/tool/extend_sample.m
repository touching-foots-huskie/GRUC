% extend sample structure:
function Y = extend_sample(y, d_step)
    seqlen = size(y, 1);
    SeqLen = d_step*seqlen;
    Y = zeros(SeqLen, 1);
    for i = 1:1:(seqlen-1)
        Y((i-1)*d_step+1:i*d_step+1) = linspace(y(i), y(i+1), d_step+1);
    end    
end