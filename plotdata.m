clear all;

load('smartfarm_firstrun.mat')

length = numel(data.temp);

figure(5);

subplot(2,1,1);
yyaxis left;
plot(1:length,data.temp)
title('Conditions Under Lighting');
ylabel('Temperature °C')
yyaxis right;
plot(1:length,data.humd)
ylabel('Humidity %')
legend('Temperature', 'Humidity')
xticks([1 95 190 284 361 457 550 644 722 778])
xticklabels({'10 Nov Fri 14:00','10 Nov Fri 22:04','11 Nov Sat 06:06','11 Nov Sat 14:05','11 Nov Sat 20:35','12 Nov Sun 04:43', '12 Nov Sun 12:35', '12 Nov Sun 20:33', '13 Mon 03:12', '13 Mon 07:56'})
xlabel('2017')

subplot(2,1,2); 
plot(1:length,data.ppfd0,'m',1:length,data.ppfdred0,'r',1:length,data.ppfdblue0,'b');
title('Light Cycle')
legend('Combined PPFD', 'PPFD Red LED', 'PPFD Blue LED')
ylabel('PPFD Sensor1 uMol / m2 / s')
xticks([1 95 190 284 361 457 550 644 722 778])
xticklabels({'10 Nov Fri 14:00','10 Nov Fri 22:04','11 Nov Sat 06:06','11 Nov Sat 14:05','11 Nov Sat 20:35','12 Nov Sun 04:43', '12 Nov Sun 12:35', '12 Nov Sun 20:33', '13 Mon 03:12', '13 Mon 07:56'})
xlabel('2017')

load('smartfarm_secondrun.mat')
length = numel(data.temp_a);
data.humd_u(find(data.humd_u>1000))=data.humd_u(find(data.humd_u>1000)-1);
data.humd_a(find(data.humd_a>1000))=data.humd_a(find(data.humd_a>1000)-1);
data.temp_u(find(data.temp_u<16))=data.temp_u(find(data.temp_u<16)-1);
data.temp_a(find(data.temp_a<16))=data.temp_a(find(data.temp_a<16)-1);


figure(1)

subplot(3,1,1);
plot(1:length,data.avg_basin1);
title('Pot 1 Avg Moisture');
xticks([1    43    89   230   277   418   465   606   651]);
xticklabels({'17 Nov Fri 16:29','Fri 20:05','18 Nov Sat 00:00','Sat 12:01','Sat 16:00','Sun 4:01','Sun 08:00','Sun 20:04','19 Nov Sun 23:54'});
xlabel('2017');
ylim([300 500]);
ylabel('Moisture Sensor (0-1023)');

subplot(3,1,2);
plot(1:length,data.avg_basin2);
title('Pot 2 Avg Moisture')
xticks([1    43    89   230   277   418   465   606   651]);
xticklabels({'17 Nov Fri 16:29','Fri 20:05','18 Nov Sat 00:00','Sat 12:01','Sat 16:00','Sun 4:01','Sun 08:00','Sun 20:04','19 Nov Sun 23:54'});
xlabel('2017');
ylim([300 500]);
ylabel('Moisture Sensor (0-1023)');

subplot(3,1,3);
plot(1:length,data.avg_basin3);
title('Pot 3 Avg Moisture');
xticks([1    43    89   230   277   418   465   606   651]);
xticklabels({'17 Nov Fri 16:29','Fri 20:05','18 Nov Sat 00:00','Sat 12:01','Sat 16:00','Sun 4:01','Sun 08:00','Sun 20:04','19 Nov Sun 23:54'});
xlabel('2017');
ylim([300 500]);
ylabel('Moisture Sensor (0-1023)');

figure(2)

subplot(2,1,1);
yyaxis left;
plot(1:length,data.temp_a)
ylim([16 30])
title('Conditions Above Lighting');
ylabel('Temperature °C')
yyaxis right;
plot(1:length,data.humd_a)
ylim([50 100])
ylabel('Humidity %')
legend('Temperature', 'Humidity')
xticks([1    43    89   230   277   418   465   606   651]);
xticklabels({'17 Nov Fri 16:29','Fri 20:05','18 Nov Sat 00:00','Sat 12:01','Sat 16:00','Sun 4:01','Sun 08:00','Sun 20:04','19 Nov Sun 23:54'});
xlabel('2017')

subplot(2,1,2);
yyaxis left;
plot(1:length,data.temp_u)
ylim([16 30])
title('Conditions Under Lighting');
ylabel('Temperature °C')
yyaxis right;
plot(1:length,data.humd_u)
ylim([50 100])
ylabel('Humidity %')
legend('Temperature', 'Humidity')
xticks([1    43    89   230   277   418   465   606   651]);
xticklabels({'17 Nov Fri 16:29','Fri 20:05','18 Nov Sat 00:00','Sat 12:01','Sat 16:00','Sun 4:01','Sun 08:00','Sun 20:04','19 Nov Sun 23:54'});
xlabel('2017')

figure(3)
suptitle('PPFD Distribution, Heatsink on Right')

subplot(4,3,10)
plot(1:length,data.ppfdred0,'r',1:length,data.ppfdblue0,'b',1:length,data.ppfd0,'m')
ylim([0 400])
xticks([]);
ylabel('PPFD uMol / m2 / s')

subplot(4,3,8)
plot(1:length,data.ppfdred1,'r',1:length,data.ppfdblue1,'b',1:length,data.ppfd1,'m')
ylim([0 400])
xticks([]);
ylabel('PPFD uMol / m2 / s')

subplot(4,3,12)
plot(1:length,data.ppfdred2,'r',1:length,data.ppfdblue2,'b',1:length,data.ppfd2,'m')
ylim([0 400])
xticks([]);
ylabel('PPFD uMol / m2 / s')

subplot(4,3,5)
plot(1:length,data.ppfdred4,'r',1:length,data.ppfdblue4,'b',1:length,data.ppfd4,'m')
ylim([0 400])
xticks([]);
ylabel('PPFD uMol / m2 / s')

subplot(4,3,1)
plot(1:length,data.ppfdred3,'r',1:length,data.ppfdblue3,'b',1:length,data.ppfd3,'m')
ylim([0 400])
xticks([]);
ylabel('PPFD uMol / m2 / s')

subplot(4,3,3)
plot(1:length,data.ppfdred5,'r',1:length,data.ppfdblue5,'b',1:length,data.ppfd5,'m')
legend('Combined PPFD', 'PPFD Red LED', 'PPFD Blue LED')
ylim([0 400])
xticks([]);
ylabel('PPFD uMol / m2 / s')

avgred = mean(data.ppfdred0+data.ppfdred1+data.ppfdred2+data.ppfdred3+data.ppfdred4+data.ppfdred5)
avgblue = mean(data.ppfdblue0+data.ppfdblue1+data.ppfdblue2+data.ppfdblue3+data.ppfdblue4+data.ppfdblue5)
avgppfd = mean(data.ppfd0+data.ppfd1+data.ppfd2+data.ppfd3+data.ppfd4+data.ppfd5)

figure(4)

plot(1:length,data.ppfdred5,'r',1:length,data.ppfdblue5,'b',1:length,data.ppfd5,'m')
legend('Combined PPFD', 'PPFD Red LED', 'PPFD Blue LED')
ylim([0 400])
xticks([]);
ylabel('PPFD uMol / m2 / s')
xticks([1    43    89   230   277   418   465   606   651]);
xticklabels({'17 Nov Fri 16:29','Fri 20:05','18 Nov Sat 00:00','Sat 12:01','Sat 16:00','Sun 4:01','Sun 08:00','Sun 20:04','19 Nov Sun 23:54'});
xlabel('2017')

