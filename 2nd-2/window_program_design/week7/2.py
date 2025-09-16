import random
import math

# 繼續第一題, 加入判斷式, 若與實際數字答案相差不到 3則提示只差一點點

def generate_random_number() -> int:
    return random.randint(0, 99)

def user_input() -> int:
    return int(input("Please enter a number: "))

def check_guess(guess: int, number: int) -> bool:
    result = False
    if number == guess:
        print("You guessed the number!")
        return True
    if number > guess:
        print("Too low!")
        result = False
    if number < guess:
        print("Too high!")
        result = False
    if math.fabs(number - guess) <= 3:
        print("You are close!")
    return result

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
    print(f"The average number of guesses is {total_guesses / count_games:.2f}")


if __name__ == "__main__":
    main()


