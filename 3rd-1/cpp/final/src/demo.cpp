#include "MLO.h"
#include <iostream>

using namespace std;

int main() {
  MLO mlo(4, 15);

  // 手動建立 6 個 jobs
  DX_INFO jobs[6] = {
    {0, 0.5, 3, 3},  // Job1: 3 res, 3 slots
    {1, 0.3, 1, 1},  // Job2: 1 res, 1 slot
    {2, 0.4, 3, 3},  // Job3: 3 res, 3 slots
    {3, 0.2, 2, 1},  // Job4: 2 res, 1 slot
    {4, 0.6, 1, 3},  // Job5: 1 res, 3 slots
    {5, 0.3, 1, 3},  // Job6: 1 res, 3 slots
  };

  cout << "Jobs:" << endl;
  for (int i = 0; i < 6; i++) {
    cout << "Job" << jobs[i].id + 1 << ": res=" << jobs[i].NoOfResourcesNeeded
         << ", slots=" << jobs[i].NoOfTimeSlotsNeeded << endl;
    mlo.scheduleFCFS(&jobs[i]);
    mlo.scheduleBF(&jobs[i]);
  }

  cout << "\n=== FCFS ===" << endl;
  mlo.fcfs->print();

  cout << "\n=== BF ===" << endl;
  mlo.bf->print();

  // Throughput
  double fcfsTp = (double)mlo.fcfs->jobCount / mlo.fcfs->horizon;
  double bfTp = (double)mlo.bf->jobCount / mlo.bf->horizon;
  cout << "\n=== Throughput ===" << endl;
  cout << "FCFS: " << mlo.fcfs->jobCount << " / " << mlo.fcfs->horizon << " = " << fcfsTp << endl;
  cout << "BF:   " << mlo.bf->jobCount << " / " << mlo.bf->horizon << " = " << bfTp << endl;

  return 0;
}
