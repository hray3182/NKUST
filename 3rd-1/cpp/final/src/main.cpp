#include "MLO.h"
#include "PKTArrivalEventGenerator.h"
#include <iomanip>
#include <iostream>

using namespace std;

int main() {

  int DEMO_ITERATION = 15;
  int NUM_RESOURCES = 4;
  int NUM_TIME_SLOTS = 50;

  PKTArrivalEventGenerator demoGen(78, 0.5, NUM_RESOURCES, 6);
  MLO demoMLO(NUM_RESOURCES, NUM_TIME_SLOTS);

  int i = 0;
  while (i < DEMO_ITERATION) {
    DX_INFO *job = demoGen.createNewArrival();
    demoMLO.scheduleFCFS(job);
    demoMLO.scheduleBF(job);
    delete job;
    i++;
  }

  cout << "\n=== FCFS Schedule ===" << endl;
  demoMLO.fcfs->print();

  cout << "\n=== BF Schedule ===" << endl;
  demoMLO.bf->print();

  // throughput = 已傳輸的總數量 / (最後一筆資料傳輸的時段編號 + 1)
  double fcfsThroughput =
      (double)demoMLO.fcfs->jobCount / demoMLO.fcfs->horizon;
  double bfThroughput = (double)demoMLO.bf->jobCount / demoMLO.bf->horizon;

  cout << "\n=== Throughput 比較 ===" << endl;
  cout << "FCFS: " << demoMLO.fcfs->jobCount << " / " << demoMLO.fcfs->horizon
       << " = " << fixed << setprecision(4) << fcfsThroughput << endl;
  cout << "BF:   " << demoMLO.bf->jobCount << " / " << demoMLO.bf->horizon
       << " = " << fixed << setprecision(4) << bfThroughput << endl;

  return 0;
}
