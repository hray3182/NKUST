# 圓的座標在-1到1之間
# 產生隨機數，範圍在-1到1之間，然後計算他們與圓心的距離有沒有小於等於1，有的話就在圓內
# 最後用圓內的點數除以總點數乘以4就可以得到π的近似值

import random

x, y = 0, 0
inside = 0
total = 1000000

for _ in range(total):
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    if x**2 + y**2 <= 1:
        inside += 1

pi = (inside / total) * 4
print(pi)