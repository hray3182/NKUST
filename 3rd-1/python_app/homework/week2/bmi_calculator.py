def get_user_input(placeholder: str) -> float:
    num = 0
    while True:
        user_input = input(placeholder)
        try:
            num = float(user_input)
            if num > 0:
                return num
        except:
            pass
        print("輸入不正確，請重新輸入")

def bmi_cal(weight: float, heigh: float):
    heigh /= 100
    return weight / heigh**2

def get_bmi_judge(bmi: float) -> str:
    bmi_threshold = [18.5, 25, 30, float('inf')]
    bmi_judge = ["體重不足", "正常", "過重", "肥胖"]
    for i in range(len(bmi_threshold)):
        if bmi < bmi_threshold[i]:
            return bmi_judge[i]


weight = get_user_input("請輸入體重(kg): ")
heigh = get_user_input("請輸入身高(cm): ")
bmi = bmi_cal(weight, heigh)
judge = get_bmi_judge(bmi)
print(f"你的bmi為{bmi:.2f}, 判斷為{judge}")

