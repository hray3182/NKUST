def get_input(placeholder) -> int:
    while True:
        try:
            input_num = int(input(placeholder))
            if input_num > 0:
                return input_num
            else:
                print("請輸入正整數")
        except ValueError:
            print("請輸入數字")
            pass


input_num = get_input("請輸入一個正整數：")
factors = []

for i in range(1, input_num + 1):
    if input_num % i == 0:
        factors.append(i)

sum = 0
for i in range(len(factors) - 1):
    sum += factors[i]


if input_num > sum:
    print("虧數")
else:
    print("盈數")
