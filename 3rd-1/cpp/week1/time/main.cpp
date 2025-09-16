#include "time.h"

int main() {
  Time time;
  time.setTime(15, 60, 5);
  time.printMilitary();
  time.printStandard();
  return 0;
}
