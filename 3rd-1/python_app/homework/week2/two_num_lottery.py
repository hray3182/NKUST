import random


def get_user_input(placeholder: str) -> int:
    num = 0
    while True:
        user_input = input(placeholder)
        try:
            num = int(user_input)
            if num >= 0 and num < 10:
                return num
        except:
            pass
        print("輸入不正確，請重新輸入")


def get_prize(num1, num2) -> int:
    right = random.sample(range(9), 2)
    print(f"開獎號碼為{right[0]}, {right[1]}")
    if right[0] == num1 and right[1] == num2:
        return 10000
    if right[0] == num2 and right[1] == num1:
        return 3000
    if num1 in right or num2 in right:
        return 1000
    return 0


num1 = 0
num2 = 0
while num1 == num2:
    num1 = get_user_input("請輸入0~9: ")
    num2 = get_user_input("請輸入0~9: ")
    if num1 == num2:
        print("不能輸入兩個相同數字，請重新輸入")

prize = get_prize(num1, num2)
print(f"您獲得${prize}元")
