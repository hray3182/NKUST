# 3.	亂數產生 1-30 之間的數字進行猜字遊戲,5 次內猜中算贏 1 次就猜中獎金 3000, 2-3 次猜中獎金 2000, 4-5 次才猜中獎金 1000, 否則就是失敗 
import random

answer = random.randint(1, 2)

try_count = 0
for i in range(5):
    guess = int(input("請猜一個 1-30 之間的數字: "))
    if guess == answer:
        print("猜中了!")
        break
    else:
        print("猜錯了!")
        try_count += 1

if try_count == 0:
    print("恭喜你贏得 3000 元!")
elif try_count == 1 or try_count == 2:
    print("恭喜你贏得 2000 元!")
elif try_count == 3 or try_count == 4:
    print("恭喜你贏得 1000 元!")
else:
    print("很抱歉, 你猜錯了!")