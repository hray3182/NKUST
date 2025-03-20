# 撰寫 BMI 計算程式, 輸入體重與身高換算成 BMI 數值

print("BMI 計算器")
print("--------------------------------")
height = float(input("請輸入身高(cm): "))
weight = float(input("請輸入體重(kg): "))

bmi = weight / (height/100 * height/100)

print(f"BMI 值為: {bmi:.2f}", end=" ")

if bmi < 18.5:
    print("體重過輕")
elif bmi >= 18.5 and bmi < 24:
    print("體重正常")
elif bmi >= 24 and bmi < 27:
    print("體重過重")
elif bmi >= 27 and bmi:
    print("輕度肥胖")
    
