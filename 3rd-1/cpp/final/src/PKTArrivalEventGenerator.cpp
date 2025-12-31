#include "PKTArrivalEventGenerator.h"

PKTArrivalEventGenerator::PKTArrivalEventGenerator(unsigned seed_in, double avg_interArrivalTime, int max_NoOfResourcesNeeded_in, int max_NoOfTimeSlotsNeeded_in)
    : arrivalTime_expRandGenerator(seed_in, 1.0 / avg_interArrivalTime), // lambda = 1 / 平均值
      arrivalRate_lambda(1.0 / avg_interArrivalTime),
      PKTCNT(0),
      masterTime(0.0),
      max_NoOfResourcesNeeded(max_NoOfResourcesNeeded_in),
      max_NoOfTimeSlotsNeeded(max_NoOfTimeSlotsNeeded_in)
{
}

DX_INFO* PKTArrivalEventGenerator::createNewArrival()
{
    DX_INFO* newJob = new DX_INFO;

    // 產生指數分布的到達間隔時間
    double interArrivalTime = arrivalTime_expRandGenerator.eRand();
    masterTime += interArrivalTime;

    // 填入工作資訊
    newJob->id = PKTCNT++;
    newJob->arrivalTime = masterTime;

    // 產生 [1, max] 之間的均勻分布整數
    newJob->NoOfResourcesNeeded = arrivalTime_expRandGenerator.uniform_rand_range(1, max_NoOfResourcesNeeded);
    newJob->NoOfTimeSlotsNeeded = arrivalTime_expRandGenerator.uniform_rand_range(1, max_NoOfTimeSlotsNeeded);

    return newJob;
}
