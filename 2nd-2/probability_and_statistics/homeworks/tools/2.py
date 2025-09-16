import numpy as np
import matplotlib.pyplot as plt

n_samples = 2000 # 要生成的常態分佈樣本數量

# --- 使用 Box-Muller 變換生成標準常態分佈樣本 ---
n_uniform_pairs = n_samples // 2

u1 = np.random.rand(n_uniform_pairs)
u2 = np.random.rand(n_uniform_pairs)

z1 = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
z2 = np.sqrt(-2 * np.log(u1)) * np.sin(2 * np.pi * u2)

generated_samples = np.concatenate((z1, z2))
generated_samples = generated_samples[:n_samples]

def standard_normal_pdf(x):
  """
  計算標準常態分佈 (mu=0, sigma=1) 在 x 點的機率密度
  """
  mu = 0
  sigma = 1
  return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-((x - mu)**2) / (2 * sigma**2))


# 創建直方圖
plt.figure(figsize=(8, 6))
plt.hist(generated_samples, bins=50, density=True, alpha=0.6, color='g', label='Generated Samples Histogram')

# 生成一系列用於繪製 PDF 的 x 值
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = standard_normal_pdf(x)
plt.plot(x, p, 'k', linewidth=2, label='Standard Normal PDF')

# 添加圖例和標題
plt.title(f'Histogram of {n_samples} Generated Standard Normal Samples vs. Custom PDF')
plt.xlabel('Value')
plt.ylabel('Density')
plt.legend()
plt.grid(True)

# 顯示圖形
plt.show()

sample_mean = np.mean(generated_samples)
sample_std = np.std(generated_samples)
print(f"生成樣本的平均值: {sample_mean:.4f}")
print(f"生成樣本的標準差: {sample_std:.4f}")