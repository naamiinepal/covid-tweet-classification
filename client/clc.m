clc;
clear all;
close all;

AmpC=10; %amplitude of the carrier
FreC=50; %frequency of the carrier
AmpM=10; %amplitudeof the message
FreM=5; %frequency of the message

ka=1;%Amplitude Sensitivity

t=[0:0.001:1];
carrier=AmpC*sin(2*pi*FreC*t);
message=AmpM*sin(2*pi*FreM*t);
AM=carrier.*(1+ka*message);

subplot(3,1,1);
plot(message);
ylabel('Message signal');

subplot(3,1,2);
plot(carrier);
ylabel('carrier');

subplot(3,1,3);
plot(AM);
ylabel('AM signal');
