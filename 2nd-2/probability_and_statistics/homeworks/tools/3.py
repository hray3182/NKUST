import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm 

# 定義雙變數常態分佈的參數 
mu_x = 0    # X 的平均值
mu_y = 0    # Y 的平均值
sigma_x = 1 # X 的標準差
sigma_y = 1 # Y 的標準差
rho = 0.8   # X 和 Y 之間的相關係數 (介於 -1 到 1 之間)

# 定義繪圖範圍 
x_range = np.linspace(mu_x - 3*sigma_x, mu_x + 3*sigma_x, 100)
y_range = np.linspace(mu_y - 3*sigma_y, mu_y + 3*sigma_y, 100)

# 創建一個網格來計算每個點的 PDF 值
X, Y = np.meshgrid(x_range, y_range)

#計算雙變數常態分佈的 PDF 值 

rho_squared = rho**2
det_cov = sigma_x * sigma_y * np.sqrt(1 - rho_squared) # 共變異數矩陣行列式的平方根

# 計算指數部分
z = ((X - mu_x) / sigma_x)**2 + ((Y - mu_y) / sigma_y)**2 - (2 * rho * (X - mu_x) * (Y - mu_y)) / (sigma_x * sigma_y)
exponent = -z / (2 * (1 - rho_squared))

# 計算完整的 PDF 值
# PDF = 1 / (2 * pi * sigma_x * sigma_y * sqrt(1 - rho^2)) * exp(exponent)
Z = (1 / (2 * np.pi * det_cov)) * np.exp(exponent)

# 繪製三維 PDF 圖 
fig = plt.figure(figsize=(12, 6))

ax1 = fig.add_subplot(121, projection='3d')
# 繪製曲面圖
surf = ax1.plot_surface(X, Y, Z, cmap=cm.viridis, linewidth=0, antialiased=False)
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Probability Density')
ax1.set_title('Bivariate Normal PDF (3D)')
# 添加顏色條
fig.colorbar(surf, shrink=0.5, aspect=5)


# 繪製等高線圖 
ax2 = fig.add_subplot(122)
# 繪製等高線圖
# levels 可以控制等高線的數量和位置
contour = ax2.contour(X, Y, Z, levels=20, cmap=cm.viridis)
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_title('Bivariate Normal PDF (Contour)')
# 添加等高線標籤
ax2.clabel(contour, inline=1, fontsize=10)
ax2.set_aspect('equal', adjustable='box') # 讓 X 和 Y 軸比例相等，等高線形狀更準確

# 顯示圖形
plt.tight_layout() 
plt.show()

# 進一步探討 
print(f"雙變數常態分佈參數: mu_x={mu_x}, mu_y={mu_y}, sigma_x={sigma_x}, sigma_y={sigma_y}, rho={rho}")