#ifndef _SCHEDULE_H_
#define _SCHEDULE_H_

class Schedule {
public:
  int **table; // 2D 陣列
  int rows;    // 資源數量
  int cols;    // 時段數量
  int horizon; // 排班邊界（最後佔用的時段+1）
  int jobCount; // 已排班工作數

  Schedule(int rows_in, int cols_in);

  int get(int r, int c);
  void set(int r, int c, int value);
  bool test(int r, int c, int numRes, int numSlots); // 檢查區塊是否可用
  void print();
};

#endif
