import random

# 生成5個減法問題


def get_input(placehold) -> int:
    while True:
        try:
            return int(input(placehold))
        except ValueError:
            print("請輸入數字")
            pass


correct = 0
times = 5

while times > 0:
    nums = random.sample(range(1, 100), 2)
    nums.sort(reverse=True)
    ans = nums[0] - nums[1]
    user_input = get_input(f"{nums[0]} - {nums[1]} = ")
    print()
    if user_input == ans:
        print("答對了")
        correct += 1
    else:
        print(f"答錯了，答案是 {ans}")
    times -= 1

print(f"總共答對 {correct} 題")
