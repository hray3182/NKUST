#ifndef TIME_H

#define TIME_H

class Time {
public:
  Time();
  void setTime(int h, int m, int s);
  void printMilitary();
  void printStandard();

private:
  int hour;
  int minute;
  int second;
};

#endif // !TIME_H
