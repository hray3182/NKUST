import random

# 隨機產生大樂透號碼1-49, 然後提示使用者輸入6個簽選號碼, 最後顯示大樂透號碼, 你簽選的號碼以及簽對了幾個號碼

def generate_lottery_numbers() -> list:
    return sorted(random.sample(range(1, 50), 6))

def user_input() -> list:
    return sorted(list(map(int, input("Please enter 6 numbers: ").split())))

def main():
    lottery_numbers = generate_lottery_numbers()
    user_numbers = user_input()
    print(f"Lottery numbers: {lottery_numbers}")
    print(f"User numbers: {user_numbers}")
    print(f"You guessed {len(set(lottery_numbers) & set(user_numbers))} numbers correctly")

if __name__ == "__main__":
    main()


