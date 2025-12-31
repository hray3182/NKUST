#ifndef _PKTARRIVALEVENTGENERATOR_H_
#define _PKTARRIVALEVENTGENERATOR_H_

#include "exponentialRand.h"

struct DX_INFO {
	long long id;
	double arrivalTime;
	int NoOfResourcesNeeded;
	int NoOfTimeSlotsNeeded;
};

class PKTArrivalEventGenerator
{
private:
	exponentialRand arrivalTime_expRandGenerator;
	double arrivalRate_lambda;	
	long long PKTCNT;	
	double masterTime;
	int max_NoOfResourcesNeeded;
	int max_NoOfTimeSlotsNeeded;

public:
	// seed_in: 自選的隨機種子值，任意設定即可
	// avg_interArrivalTime: 兩個連續工作的間隔時間平均值
	// max_NoOfResourcesNeeded_in: 工作需要的資源最大數量，假設最小為1
	// max_NoOfTimeSlotsNeeded_in: 工作需要的時段最大數量，假設最小為1
	PKTArrivalEventGenerator(unsigned seed_in, double avg_interArrivalTime, int max_NoOfResourcesNeeded_in, int max_NoOfTimeSlotsNeeded_in);	// initialization
	DX_INFO* createNewArrival();	// call this to generate a new job
};

#endif
