import random

# 以亂數產生0-99之間整數, 然後讓使用者猜一個數字, 如果猜中告訴猜中, 詢問是否要繼續此遊戲, 
# 若猜錯則提示猜的數字太大或太小, 繼續猜直到猜中為止, 最後統計總共玩了幾次, 每一次各猜幾次才猜中, 
# 平均猜中的次數


def generate_random_number() -> int:
    return random.randint(0, 99)


def user_input() -> int:
    return int(input("Please enter a number: "))


def check_guess(guess: int, number: int) -> bool:
    if number == guess:
        print("You guessed the number!")
        return True
    if number > guess:
        print("Too low!")
        return False
    if number < guess:
        print("Too high!")
        return False


def main():
    keep = False
    count_games = 0
    total_guesses = 0
    while not keep:
        number = generate_random_number()
        guess = user_input()
        count_guesses = 1
        while not check_guess(guess, number):
            guess = user_input()
            count_guesses += 1
        count_games += 1
        total_guesses += count_guesses
        keep = input("Do you want to keep playing? (y/n): ") == "n"

    print(f"You played {count_games} games!")
    # print average number of guesses
    print(
        f"The average number of guesses is {total_guesses / count_games:.2f}")


if __name__ == "__main__":
    main()
