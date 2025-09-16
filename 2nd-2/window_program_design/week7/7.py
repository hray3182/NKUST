# 產生一6*6 的二維陣列, 其元素不是0 就是 1, 然後判斷每一列和每一行是否有偶數個 1

import random

def generate_matrix(rows: int, cols: int) -> list:
    return [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]

def check_matrix(matrix: list):
    row_counts = [0] * len(matrix)
    col_counts = [0] * len(matrix[0])
    
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 1:
                row_counts[i] += 1
                col_counts[j] += 1
    
    # 顯示每一列的結果
    print("\n檢查每一列：")
    for i, count in enumerate(row_counts):
        print(f"第 {i+1} 列有 {count} 個1，{'是' if count % 2 == 0 else '不是'}偶數")
    
    # 顯示每一行的結果
    print("\n檢查每一行：")
    for j, count in enumerate(col_counts):
        print(f"第 {j+1} 行有 {count} 個1，{'是' if count % 2 == 0 else '不是'}偶數")

def print_matrix(matrix: list):
    for row in matrix:
        print(' '.join(map(str, row)))

matrix = generate_matrix(6, 6)
print("產生的矩陣：")
print_matrix(matrix)
check_matrix(matrix)


