import random

# 使用者輸入頭擲骰子的次數, 然後統計每一個數字出現的百分比

def input_count() -> int:
    return int(input("Please enter the count of rolls the dice: "))

def generate_random_number() -> int:
    return random.randint(1, 6)

def main():
    count = input_count()
    result = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
    for _ in range(count):
        number = generate_random_number()
        result[number] += 1
    for key, value in result.items():
        print(f"{key}: {value / count * 100:.2f}%")

if __name__ == "__main__":
    main()



