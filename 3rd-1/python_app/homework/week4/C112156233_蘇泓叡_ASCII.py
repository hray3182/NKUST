import random

# Const
all_visible_ascii = [i for i in range(32, 127)]
uppercase = [i for i in range(65, 91)]
lowercase = [i for i in range(97, 123)]
numbers = [i for i in range(48, 58)]


def get_random_ascii(ascii_list):
    return chr(random.choice(ascii_list))


def get_user_input():
    while True:
        user_input = input(
            "Choose character set:\n1. All visible ASCII characters\n2. Uppercase letters (A-Z)\n3. Lowercase letters (a-z)\n4. Numbers (0-9)\nEnter choice (1-4): "
        )
        if user_input in ["1", "2", "3", "4"]:
            return int(user_input)
        else:
            print("Invalid input. Please enter a number between 1 and 4.")


choice = get_user_input()
ascii_list = []

if choice == 1:
    ascii_list = all_visible_ascii
elif choice == 2:
    ascii_list = uppercase
elif choice == 3:
    ascii_list = lowercase
elif choice == 4:
    ascii_list = numbers

random_char = get_random_ascii(ascii_list)
print(f"Random character: {random_char}")
