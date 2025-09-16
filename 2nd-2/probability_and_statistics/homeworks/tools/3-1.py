import matplotlib.pyplot as plt
import numpy as np 

# 設定柏努利分佈的參數 
p = 0.3 # 成功的機率

# 確保 p 在 (0, 1) 之間
if not (0 < p < 1):
    raise ValueError("參數 p 必須介於 0 和 1 之間 (不包含 0 和 1)")

# 定義柏努利隨機變數的可能取值和對應機率 
outcomes = [0, 1]
pmf_values = [1 - p, p] # P(X=0) = 1-p, P(X=1) = p


# 定義 x 值來繪製這個階梯函數
cdf_x = [-0.5, 0, 0, 1, 1, 1.5] # 在步階變化的前後都包含點
cdf_y = [0, 0, 1 - p, 1 - p, 1, 1] # 對應的累積機率值

# 繪製 PMF 和 CDF 圖形 

plt.figure(figsize=(8, 6))

# 繪製 PMF (使用垂直線表示離散點的機率)
plt.vlines(outcomes, 0, pmf_values, colors='b', lw=3, label='PMF')
plt.plot(outcomes, pmf_values, "bo") # 在點的位置加上圓點

# 繪製 CDF (使用 step 函數表示階梯狀)
plt.step(cdf_x, cdf_y, where='post', color='r', lw=2, label='CDF')

# 添加圖形元素 
plt.title(f'Bernoulli Distribution (p={p}) PMF and CDF')
plt.xlabel('Outcome (x)')
plt.ylabel('Probability / Cumulative Probability')
plt.xticks(outcomes) # 確保 x 軸顯示 0 和 1
plt.yticks([0, 1 - p, 1]) # 確保 y 軸顯示重要的機率值
plt.legend()
plt.grid(True)
plt.ylim(-0.05, 1.05) # 稍微擴大 y 軸範圍，讓圖形更好看

# 顯示圖形
plt.show()