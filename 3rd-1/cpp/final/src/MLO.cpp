#include "MLO.h"
#include <cmath>
#include <algorithm>

using namespace std;

MLO::MLO(int rows, int cols) {
  fcfs = new Schedule(rows, cols);
  bf = new Schedule(rows, cols);
}

void MLO::scheduleFCFS(DX_INFO *job) {
  int earliest = (int)ceil(job->arrivalTime);
  // 從上一個 job 的開始位置搜索，看是否有剩餘 row 可並行
  int startCol = max(fcfs->lastJobStartCol, earliest);
  int numRows = job->NoOfResourcesNeeded;
  int numCols = job->NoOfTimeSlotsNeeded;

  for (int col = startCol; col + numCols <= fcfs->cols; col++) {
    for (int row = fcfs->rows - numRows; row >= 0; row--) {  // 從底部往上搜索
      if (fcfs->test(row, col, numRows, numCols)) {
        for (int r = row; r < row + numRows; r++) {
          for (int c = col; c < col + numCols; c++) {
            fcfs->set(r, c, job->id + 1);
          }
        }
        fcfs->lastJobStartCol = col;  // 更新上一個 job 的開始位置
        int endCol = col + numCols;
        if (endCol > fcfs->horizon) {
          fcfs->horizon = endCol;
        }
        fcfs->jobCount++;
        return;
      }
    }
  }
}

void MLO::scheduleBF(DX_INFO *job) {
  int earliest = (int)ceil(job->arrivalTime);
  int numRows = job->NoOfResourcesNeeded;
  int numCols = job->NoOfTimeSlotsNeeded;

  for (int col = earliest; col + numCols <= bf->cols; col++) {
    for (int row = bf->rows - numRows; row >= 0; row--) {  // 從底部往上搜索
      if (bf->test(row, col, numRows, numCols)) {
        for (int r = row; r < row + numRows; r++) {
          for (int c = col; c < col + numCols; c++) {
            bf->set(r, c, job->id + 1);
          }
        }
        int endCol = col + numCols;
        if (endCol > bf->horizon) {
          bf->horizon = endCol;
        }
        bf->jobCount++;
        return;
      }
    }
  }
}
