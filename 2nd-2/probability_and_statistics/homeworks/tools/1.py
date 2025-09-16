import numpy as np

n_samples = 100

x_samples_independent = np.random.randn(n_samples)
y_samples_independent = np.random.randn(n_samples)

# 設定樣本數量
n_samples = 100

# 生成 X 的隨機樣本 
x_samples_correlated = np.random.randn(n_samples)

# 生成 Y 的隨機樣本，使其與 X 有線性關係並加入雜訊
# 假設 Y = X + 雜訊
noise = np.random.randn(n_samples) * 0.5 # 雜訊的標準差可以調整以控制相關性強度
y_samples_correlated =  x_samples_correlated + noise

# 計算獨立樣本的相關係數矩陣
correlation_matrix_independent = np.corrcoef(x_samples_independent, y_samples_independent)
sample_correlation_independent = correlation_matrix_independent[0, 1] # 取非對角線的值

print(f"獨立樣本的樣本相關係數: {sample_correlation_independent}")

# 計算有相關性樣本的相關係數矩陣
correlation_matrix_correlated = np.corrcoef(x_samples_correlated, y_samples_correlated)
sample_correlation_correlated = correlation_matrix_correlated[0, 1] # 取非對角線的值

print(f"有相關性樣本的樣本相關係數: {sample_correlation_correlated}")