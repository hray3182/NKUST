#ifndef _MLO_H_
#define _MLO_H_

#include "Schedule.h"
#include "PKTArrivalEventGenerator.h"

class MLO {
public:
  Schedule *fcfs;
  Schedule *bf;

  MLO(int rows, int cols);

  void scheduleFCFS(DX_INFO *job);
  void scheduleBF(DX_INFO *job);
};

#endif
