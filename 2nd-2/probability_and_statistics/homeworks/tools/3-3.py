import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

# --- 定義繪製雙變數常態分佈圖形的函數 ---
def plot_bivariate_normal(mu_x, mu_y, sigma_x, sigma_y, rho):
    """
    根據給定的參數繪製雙變數常態分佈的 PDF 三維圖和等高線圖。

    Args:
        mu_x (float): X 的平均值
        mu_y (float): Y 的平均值
        sigma_x (float): X 的標準差
        sigma_y (float): Y 的標準差
        rho (float): X 和 Y 之間的相關係數
    """
    if abs(rho) >= 1:
         print(f"警告: 相關係數 rho={rho} 無效，必須介於 -1 和 1 之間 (不包含)。跳過此組參數。")
         return

    # 定義繪圖範圍
    x_range = np.linspace(mu_x - 4*sigma_x, mu_x + 4*sigma_x, 100) # 擴大範圍以便觀察
    y_range = np.linspace(mu_y - 4*sigma_y, mu_y + 4*sigma_y, 100) # 擴大範圍以便觀察
    X, Y = np.meshgrid(x_range, y_range)

    # 計算雙變數常態分佈的 PDF 值
    rho_squared = rho**2
    det_cov = sigma_x * sigma_y * np.sqrt(1 - rho_squared)

    z = ((X - mu_x) / sigma_x)**2 + ((Y - mu_y) / sigma_y)**2 - (2 * rho * (X - mu_x) * (Y - mu_y)) / (sigma_x * sigma_y)
    exponent = -z / (2 * (1 - rho_squared))
    Z = (1 / (2 * np.pi * det_cov)) * np.exp(exponent)

    # --- 繪製圖形 ---
    fig = plt.figure(figsize=(14, 6))
    fig.suptitle(f'Bivariate Normal Distribution: mu_x={mu_x}, mu_y={mu_y}, sigma_x={sigma_x}, sigma_y={sigma_y}, rho={rho}', fontsize=14)

    # 繪製三維 PDF 圖
    ax1 = fig.add_subplot(121, projection='3d')
    surf = ax1.plot_surface(X, Y, Z, cmap=cm.viridis, linewidth=0, antialiased=False)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Probability Density')
    ax1.set_title('3D PDF Plot')
    fig.colorbar(surf, shrink=0.5, aspect=5, label='Density')
    ax1.set_zlim(0, Z.max() * 1.1) # 固定 Z 軸範圍以便比較不同圖

    # 繪製等高線圖
    ax2 = fig.add_subplot(122)
    contour = ax2.contour(X, Y, Z, levels=15, cmap=cm.viridis) # 調整等高線數量
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_title('Contour Plot')
    ax2.clabel(contour, inline=1, fontsize=9)
    ax2.set_aspect('equal', adjustable='box')
    ax2.set_xlim(x_range.min(), x_range.max()) # 確保等高線圖範圍與三維圖一致
    ax2.set_ylim(y_range.min(), y_range.max()) # 確保等高線圖範圍與三維圖一致


    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # 調整佈局，為標題留出空間
    plt.show()

# --- 根據文件中的參數進行繪圖和觀察 ---

# 文件中提出的參數組合
parameter_sets = [
    (0, 0, 1, 1, 0),
    (0, 0, 1, 1, 0.9),
    (0, 0, 1, 1, -0.9),
    (0, 0, 1, 2, 0),
    (0, 0, 2, 1, 0),
    (1, 2, 1, 1, 0)
]

# 逐一繪製每一組參數對應的圖形
for params in parameter_sets:
    plot_bivariate_normal(*params) # 使用 *params 將元組解包作為函數參數