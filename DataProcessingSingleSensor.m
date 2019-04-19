%% Data Import
%fileID = fopen('/home/bryan/Research_Project/StairsTest2.txt');
fileID = fopen('/Users/ak/Downloads/KneeTest1/WalkingTest.txt');
power = [];
reading = [];
capc = [];
time = [];
line = fgetl(fileID); %get first line and discard
line = fgetl(fileID);
while (line ~= -1)
    data = textscan(line,'%*f %*s %d %d %f %f','Delimiter',',/t');
    power = [power data{1}];
    reading = [reading data{2}];
    capc = [capc data{4}];
    time = [time data{3}];
    line = fgetl(fileID);
end
fclose(fileID);


%% Data Plot
%{
%filter
windowWidth = 1;
kernal = ones(windowWidth,1) / windowWidth;
out = filter(kernal, 1, capc);
%}

%remove jumps in data

for i=2:length(reading)-1
    currentSlope = (capc(i) - capc(i-1))/(time(i) - time(i-1))
    adjSlope = (capc(i+1) - capc(i-1))/(time(i+1) - time(i-1))
    factor = 0.25 %adjust this based on presence of peaks
    if currentSlope/factor > adjSlope || currentSlope*factor < adjSlope
        capc(i) = (capc(i-1) + capc(i+1)) / 2
    end
end



%Cuts out the data wanted given time values
tMin = 0.5;
tMax = 6;

a=1
while time(a)< tMin
    a=a+1
end
gMin = reading(a) - reading(1)

a=1
while time(a)< tMax
    a=a+1
end
gMax = reading(a) - reading(1)


figure(1)
%plot(reading(gMin:gMax), capc(gMin:gMax))
plot(time(gMin:gMax)-time(gMin), capc(gMin:gMax))
grid on
grid minor
title('Walking Test')
xlabel('Time (s)')
ylabel('Capacitance (nF)')

%% Packet Loss Analysis
%{
packetsDropped = []; % dropped packets, 1 = dropped, 0 = received
n = reading(1);
for i = 1:length(reading)
    while(n < reading(i))
        packetsDropped = [packetsDropped 1];
        n = n+1;
    end
    packetsDropped = [packetsDropped 0];
    n = n+1;
end

plot(packetsDropped)
%}