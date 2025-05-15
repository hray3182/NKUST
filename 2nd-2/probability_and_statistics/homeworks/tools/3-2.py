import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm 

# 定義雙變數常態分佈的參數 
mu_x = 0
mu_y = 0
sigma_x = 1
sigma_y = 1
rho = 0.8   # 相關係數

# 定義繪圖範圍和網格 
x_range = np.linspace(mu_x - 3*sigma_x, mu_x + 3*sigma_x, 100)
y_range = np.linspace(mu_y - 3*sigma_y, mu_y + 3*sigma_y, 100)
X, Y = np.meshgrid(x_range, y_range)

# 計算雙變數常態分佈的 PDF 值 
if abs(rho) == 1:
    raise ValueError("相關係數不能為 1 或 -1")

rho_squared = rho**2
det_cov = sigma_x * sigma_y * np.sqrt(1 - rho_squared)

z = ((X - mu_x) / sigma_x)**2 + ((Y - mu_y) / sigma_y)**2 - (2 * rho * (X - mu_x) * (Y - mu_y)) / (sigma_x * sigma_y)
exponent = -z / (2 * (1 - rho_squared))

Z = (1 / (2 * np.pi * det_cov)) * np.exp(exponent)

# 繪製等高線圖 

plt.figure(figsize=(6, 6)) # 單獨繪製等高線圖，可以調整圖形大小

ax2 = plt.subplot(111) # 創建一個子圖 (1行1列第1個)
# 繪製等高線圖
contour = ax2.contour(X, Y, Z, levels=20, cmap=cm.viridis)
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_title('Bivariate Normal PDF (Contour)')
# 添加等高線標籤
ax2.clabel(contour, inline=1, fontsize=10)
# 確保 X 和 Y 軸比例相等，這樣等高線的橢圓形狀才不會變形
ax2.set_aspect('equal', adjustable='box')

# 顯示圖形
plt.tight_layout()
plt.show()