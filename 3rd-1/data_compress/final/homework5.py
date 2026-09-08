import numpy as np


def dct_2d(matrix):
    n = matrix.shape[0]

    # 建立 DCT 基礎矩陣
    dct_basis = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i == 0:
                dct_basis[i, j] = np.sqrt(1 / n)
            else:
                dct_basis[i, j] = np.sqrt(2 / n) * np.cos(
                    (np.pi * i * (2 * j + 1)) / (2 * n)
                )

    # DCT 轉換: T * matrix * T^T
    dct_matrix = dct_basis @ matrix @ dct_basis.T

    return dct_matrix


def main():
    # 輸入資料：8x8 矩陣
    input_matrix = np.array(
        [
            [139, 144, 149, 153, 155, 155, 155, 155],
            [144, 151, 153, 156, 159, 156, 156, 156],
            [150, 155, 160, 163, 158, 156, 156, 156],
            [159, 161, 162, 160, 160, 159, 159, 159],
            [159, 160, 161, 162, 162, 155, 155, 155],
            [161, 161, 161, 161, 160, 157, 157, 157],
            [162, 162, 161, 163, 162, 157, 157, 157],
            [162, 162, 161, 161, 163, 158, 158, 158],
        ],
        dtype=float,
    )

    dct_result = dct_2d(input_matrix)

    print("Output")
    print(np.round(dct_result, 2))


if __name__ == "__main__":
    main()
