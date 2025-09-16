# 以不定數迴圈讀取學生的分數於串列, 接著以下方給成績:
# (1) >=90, A 
# (2) >=80, B
# (3) >=70, C 
# (4) >=60, D 
# (5) 其他 F

scores = []  # 建立空串列儲存分數

print("請輸入學生成績（輸入 -1 結束）：")
while True:
    try:
        score = float(input("請輸入分數："))
        if score == -1:
            break
        if score < 0 or score > 100:
            print("分數必須在 0-100 之間，請重新輸入")
            continue
        scores.append(score)
    except ValueError:
        print("請輸入有效的數字")
        continue

print("\n成績轉換結果：")
for i, score in enumerate(scores, 1):
    if score >= 90:
        grade = 'A'
    elif score >= 80:
        grade = 'B'
    elif score >= 70:
        grade = 'C'
    elif score >= 60:
        grade = 'D'
    else:
        grade = 'F'
    print(f"學生 {i}: 分數 {score} -> 成績 {grade}")
