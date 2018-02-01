import math;
import random;
import os;
import sys;
import argparse;
import math;

L = 1000000;
C = 12000;
T = 10000;

def exponentialRandom(generatedParameter):
	return -math.log(1.0 - random.random())/generatedParameter

def findLambda(ro):
	return ro*L/C;

def generateEventList(myLambda):
	packetArrival = exponentialRandom(myLambda);
	packetLength = exponentialRandom(1.0/C);
	packetService = packetLength/L;
	packetDeparture = packetArrival + packetService;

	packetArrivalArray = [];
	packetArrivalArray.append(packetArrival);
	packetDepartureArray = [];
	packetDepartureArray.append(packetDeparture);

	while(packetArrival < T):
		nextPacketArrival = exponentialRandom(myLambda);
		packetArrival += nextPacketArrival;
		packetLength = exponentialRandom(1.0/C);
		packetService = packetLength/L;

		packetArrivalArray.append(packetArrival);

		if(packetArrival < packetDepartureArray[-1]):
			packetDepartureArray.append(packetDepartureArray[-1] + packetService);
		else:
			packetDepartureArray.append(packetArrival + packetService);

	observerArrival = exponentialRandom(4*myLambda);
	observerArray = [];
	observerArray.append(observerArrival);
	while(observerArrival < T):
		nextObserverArrival = exponentialRandom(myLambda);
		observerArrival += nextObserverArrival;
		observerArray.append(observerArrival);

	eventList = [];
	for x in packetArrivalArray:
		eventList.append(["Arrival",x]);
	for x in packetDepartureArray:
		eventList.append(["Departure",x]);
	for x in observerArray:
		eventList.append(["Observer",x]);

	return eventList

def generateEventListFinite(myLambda):
	packetArrival = exponentialRandom(myLambda);

	packetArrivalArray = [];
	packetArrivalArray.append(packetArrival);

	while(packetArrival < T):
		nextPacketArrival = exponentialRandom(myLambda);
		packetArrival += nextPacketArrival;
		packetArrivalArray.append(packetArrival);

	observerArrival = exponentialRandom(4*myLambda);
	observerArray = [];
	observerArray.append(observerArrival);
	while(observerArrival < T):
		nextObserverArrival = exponentialRandom(myLambda);
		observerArrival += nextObserverArrival;
		observerArray.append(observerArrival);

	eventList = [];
	for x in packetArrivalArray:
		eventList.append(["Arrival",x]);
	for x in observerArray:
		eventList.append(["Observer",x]);

	return eventList


def infinite(ro):
	myLambda = findLambda(ro);
	events = generateEventList(myLambda);

	events = sorted(events, key=lambda x: x[1]);

	arrivals = 0;
	departures = 0;
	observations = 0;
	idles = 0;
	numberofPacketsinQueue = [];

	for x in events:
		if(x[0] == "Arrival"):
			arrivals = arrivals + 1;
		if(x[0] == "Departure"):
			departures = departures + 1;
		if(x[0] == "Observer"):
			observations = observations + 1;
			numPackets = arrivals - departures;

			if (numPackets == 0 ):
				idles = idles + 1;
			numberofPacketsinQueue.append(numPackets);


	averageNumberofPackets = float(sum(numberofPacketsinQueue)) / float(len(numberofPacketsinQueue))
	idle = idles / float(len(numberofPacketsinQueue))


	print("Pidle: " + str(idle) + " Average number of Packets: " + str(averageNumberofPackets))
	print("Arrivals: " + str(arrivals) + " Departure: " + str(departures)+ " observations: " + str(observations) + " idles: " + str(idles))

def finite(ro, K):
	myLambda = findLambda(ro);
	events = generateEventListFinite(myLambda);

	events = sorted(events, key=lambda x: x[1], reverse=True);

	arrivals = 0;
	departures = 0;
	observations = 0;
	idles = 0;
	packetsDropped = 0;
	packetsGenerated = 0;
	queueCount =0;
	derpartureTime = 0;
	lastDeparture = 0;
	numberofPacketsinQueue = [];
	totalNumberofAllPackets = 0;

	while(events):

		x = events.pop();

		if(x[0] == "Arrival"):
			totalNumberofAllPackets = totalNumberofAllPackets + 1;
			if (queueCount < K):
				packetLength = exponentialRandom(1.0/C);
				packetService = packetLength/L;

				if(queueCount == 0):
					derpartureTime = x[1] + packetService
				else:
					derpartureTime = lastDeparture + packetService

				lastDeparture = derpartureTime;


				tempIndex = len(events) - 1;
				if (tempIndex >= 0):
					tempItem = events[tempIndex]
					while(tempItem[1] < derpartureTime):
						tempIndex = tempIndex - 1;
						if(tempIndex >= 0):
							tempItem = events[tempIndex];
						else:
							break;

				events.insert(tempIndex+1,["Departure", derpartureTime]);
				

				
				arrivals = arrivals + 1;
				queueCount = queueCount + 1;
			else:
				packetsDropped = packetsDropped + 1;

		if(x[0] == "Departure"):
			departures = departures + 1;
			queueCount = queueCount - 1;
		if(x[0] == "Observer"):
			observations = observations + 1;

			if (queueCount == 0 ):
				idles = idles + 1;
			numberofPacketsinQueue.append(queueCount);

	
	averageNumberofPackets = float(sum(numberofPacketsinQueue)) / float(len(numberofPacketsinQueue))
	ploss = packetsDropped / float(totalNumberofAllPackets)


	print("Ploss: " + str(ploss) + " Average number of Packets: " + str(averageNumberofPackets))
	print("Arrivals: " + str(arrivals) + " Departure: " + str(departures)+ " observations: " + str(observations) + " idles: " + str(idles))


def main():
	K = [5,10,40];

	range1 = [];
	range2 = [];
	range3 = [];
	
	for i in range(8):
		range1.append(0.25+(i*0.1));

	for i in range(11):
		range2.append(0.5+(i*0.1));

	for i in range(17):
		range3.append(0.4+(i*0.1));

	for i in range(15):
		range3.append(2.2+(i*0.2));

	for i in range(12):
		range3.append(5.4+(i*0.4));


	#Exponential Random Number Portion of Lab
	print("For Question 1!")
	randomNumberGenerator = [];

	for i in range(1000):
		randomNumberGenerator.append(exponentialRandom(75));

	whatisMean = sum(randomNumberGenerator) / len(randomNumberGenerator);
	whatisVariance = sum([(x - whatisMean) ** 2 for x in randomNumberGenerator]) / len(randomNumberGenerator)

	print("Variance of ERN: " + str(whatisMean));
	print("Mean of ERN: " + str(whatisVariance))


	print ("For Question 3!");
	for x in range1:
		infinite(x);

	print ("For Question 4!");
	infinite(1.2);


	print ("For Question 6!");
	for x in K:
		for y in range2:
			#print ("For K: " + str (round(x,2)) + " and ro: " + str(round(y,2)) );
			finite(y,x);

	#print ("For Question 6 Part 2!");
	#for x in K:
	#	for y in range3:
	#		#print ("For K: " + str (round(x,2)) + " and ro: " + str(round(y,2)) );
	#		finite(y,x);




if __name__ == '__main__':
	main();

