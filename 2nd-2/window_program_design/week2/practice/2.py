# 2.	1-100 累加, 不含 3 的倍數與 5 的倍數, 並計算總共累計幾筆數字

sum = 0
count = 0

for i in range(1, 101):
    if i % 3 == 0 or i % 5 == 0:
        continue
    sum += i
    count += 1

print(f"總和為: {sum}, \n總共累計幾筆數字: {count}")
