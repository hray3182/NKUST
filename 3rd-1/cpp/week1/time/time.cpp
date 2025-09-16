#include <iostream>

using namespace std;

#include "time.h"

Time::Time() {
  this->hour = 0;
  this->minute = 0;
  this->second = 0;
}

void Time::setTime(int h, int m, int s) {

  this->hour = (h < 24 && h >= 0 ? h : 0);
  this->minute = (0 < m && m < 60 ? m : 0);
  this->second = (0 < s && s < 60 ? s : 0);
}

void Time::printMilitary() {
  cout << (this->hour < 10 ? "0" : "") << this->hour << ":"
       << (this->minute < 10 ? "0" : "") << this->minute << ":"
       << (this->second < 10 ? "0" : "") << this->minute << endl;
}

void Time::printStandard() {
  cout << (this->hour % 12 < 10 ? "0" : "")
       << (this->hour < 12 ? this->hour : this->hour % 12) << ":"
       << (this->minute < 10 ? "0" : "") << this->minute << ":"
       << (this->second < 10 ? "0" : "") << this->second << " "
       << (this->hour < 12 ? "AM" : "PM") << endl;
}
