import random

# 隨機產生大樂透號碼1-49, 然後提示使用者輸入6個簽選號碼, 最後顯示大樂透號碼, 你簽選的號碼以及簽對了幾個號碼

def generate_lottery_numbers() -> list:
    return sorted(random.sample(range(1, 50), 6))

def user_input() -> list:
    check= False
    while not check:
        user_numbers = sorted(list(map(int, input("Please enter 6 numbers and split by space: ").split())))
        if len(user_numbers) == 6:
            check = True
    return user_numbers

def check_prize(num_of_hits: int) -> int:
    if num_of_hits == 6:
        return 23236441
    if num_of_hits == 5:
        return 1841913
    if num_of_hits == 4:
        return 2000
    if num_of_hits == 3:
        return 400

def main():
    lottery_numbers = generate_lottery_numbers()
    user_numbers = user_input()
    print(f"Lottery numbers: {lottery_numbers}")
    print(f"User numbers: {user_numbers}")
    hits = len(set(lottery_numbers) & set(user_numbers))
    print(f"You guessed {hits} numbers correctly")
    print(f"You won {check_prize(hits)} dollars")

if __name__ == "__main__":
    main()


