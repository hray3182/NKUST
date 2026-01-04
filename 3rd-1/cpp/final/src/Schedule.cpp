#include "Schedule.h"
#include <iomanip>
#include <iostream>

using namespace std;

Schedule::Schedule(int rows_in, int cols_in) : rows(rows_in), cols(cols_in), horizon(0), jobCount(0), lastJobStartCol(1) {
  table = new int *[rows];
  for (int i = 0; i < rows; i++) {
    table[i] = new int[cols];
    for (int j = 0; j < cols; j++) {
      table[i][j] = 0;
    }
  }
}

int Schedule::get(int r, int c) { return table[r][c]; }

void Schedule::set(int r, int c, int value) { table[r][c] = value; }

// 檢查從 (r, c) 開始的 numRes x numSlots 區塊是否都是空的
bool Schedule::test(int r, int c, int numRes, int numSlots) {
  if (r + numRes > rows || c + numSlots > cols) {
    return false;
  }
  for (int i = r; i < r + numRes; i++) {
    for (int j = c; j < c + numSlots; j++) {
      if (table[i][j] != 0) {
        return false;
      }
    }
  }
  return true;
}

void Schedule::print() {
  cout << "R\\T";
  for (int c = 1; c < cols; c++) {
    cout << setw(3) << c - 1;  // 顯示為 0, 1, 2...
  }
  cout << endl;

  for (int r = 0; r < rows; r++) {
    cout << setw(2) << r << " ";
    for (int c = 1; c < cols; c++) {  // 從 col 1 開始印
      if (table[r][c] == 0) {
        cout << setw(3) << ".";
      } else {
        cout << setw(3) << table[r][c];
      }
    }
    cout << endl;
  }
}
