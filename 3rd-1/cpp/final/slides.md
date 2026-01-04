# 多路鏈結平行傳輸
## easy FCFS + backfilling 排班

網路程式設計實務 期末專題

姓名：XXX
學號：CXXXXXXX
日期：2025/01/XX

---

# 背景與目標

## Wi-Fi 7 MLO (Multi-Link Operation)
- 傳統 Wi-Fi：同一時間只能用一種頻段
- Wi-Fi 7：可同時使用多個頻道傳輸

## 專題目標
- 用 **2D 陣列**實作排班表
- 比較 **FCFS** 和 **Backfilling** 兩種排班演算法

---

# 2D 陣列排班表

```cpp
// 建立 2D 陣列
int** table;
int rows = 4;
int cols = 10;

// 動態配置記憶體
table = new int*[rows];
for (int i = 0; i < rows; i++) {
    table[i] = new int[cols];
    for (int j = 0; j < cols; j++) {
        table[i][j] = 0;  // 初始化為 0 (空閒)
    }
}

// 存取方式
table[0][2] = 1;  // 資源 0, 時段 2 分配給工作 1

// 0 = 空閒, 其他數字 = 工作 ID
```

---

# 類別設計

## Class Schedule
```cpp
int** table;         // 2D 陣列
int rows, cols;      // 大小
int horizon;         // 排班邊界
int jobCount;        // 已排班數
int lastJobStartCol; // 上一個工作開始的 col

get(), set(), test(), print()
```

## Class MLO
```cpp
Schedule* fcfs; // FCFS 排班表
Schedule* bf;   // BF 排班表

scheduleFCFS(), scheduleBF()
```

---

# FCFS vs Backfilling

## FCFS (First Come First Served)
- 新工作從 **上一個工作的開始位置** 開始排
- 可利用同一時段剩餘的 row，但不回填更早的空隙

## Backfilling
- 從 **到達時間** 開始找空位
- 可以回填所有空隙

![FCFS vs BF](圖示)

---

# 排班表展示 - FCFS

```
R\T  0  1  2  3  4  5  6  7  8  9
 0   2  .  .  .  .  .  6  6  6  .
 1   1  1  1  3  3  3  5  5  5  .
 2   1  1  1  3  3  3  4  .  .  .
 3   1  1  1  3  3  3  4  .  .  .
```

- **horizon**: 10
- Job2 利用 Job1 剩餘的 row 0
- Job5, Job6 利用 Job4 剩餘的 row

---

# 排班表展示 - Backfilling

```
R\T  0  1  2  3  4  5  6  7
 0   2  5  5  5  6  6  6  .
 1   1  1  1  3  3  3  .  .
 2   1  1  1  3  3  3  4  .
 3   1  1  1  3  3  3  4  .
```

- **horizon**: 8
- Job2, Job5, Job6 回填到 row 0

---

# Throughput 比較

|          | FCFS  | Backfilling |
|----------|-------|-------------|
| 已排班數 | 6     | 6           |
| 最後時段 | 10    | 8           |
| **Throughput** | **0.60** | **0.75** |

$$Throughput = \frac{已排班工作數}{horizon}$$

**結論：Backfilling 效率比 FCFS 高約 25%**

---

# Demo

現場執行程式展示

```bash
make run
```

---

# 謝謝
