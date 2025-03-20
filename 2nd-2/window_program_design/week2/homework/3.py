# 撰寫洛杉磯與台灣的時差, 輸入洛杉磯時間計算台北時間以及輸入台北時間輸出洛杉磯時間

los_angeles_time = int(input("請輸入洛杉磯時間: "))
taipei_time = (los_angeles_time + 16) % 24

print(f"台北時間為: {taipei_time}")