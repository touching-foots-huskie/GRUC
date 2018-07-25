% zero phase filter:
function y = noise_filt(x)
% filt 50HZ| 100HZ and more than 50HZ
d1 = designfilt('bandstopiir','FilterOrder',20,'HalfPowerFrequency1',49,'HalfPowerFrequency2',51, 'SampleRate',5000);
d2 = designfilt('bandstopiir','FilterOrder',20,'HalfPowerFrequency1',99,'HalfPowerFrequency2',101, 'SampleRate',5000);
d3 = designfilt('lowpassiir','FilterOrder',8, 'PassbandFrequency',50,'PassbandRipple',0.2, 'SampleRate',5000); 
y = filtfilt(d1,x);
% y = filtfilt(d2,y); % because I filt more than 50HZ, than I don't need
% filt 100HZ
y = filtfilt(d3,y);
end
