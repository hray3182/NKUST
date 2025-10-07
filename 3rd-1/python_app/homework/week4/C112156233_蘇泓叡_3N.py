def three_n_plus_one(number, result):
    result.append(number)

    if number == 1:
        return result

    if number % 2 == 0:
        return three_n_plus_one(number // 2, result)
    else:
        return three_n_plus_one(3 * number + 1, result)


def get_user_input():
    while True:
        try:
            user_input = input(
                "Enter two positive integer and split them with comma\nexample: 1, 10\ninput: "
            )
            split_input = user_input.split(",")
            return (int(split_input[0]), int(split_input[1]))

        except ValueError:
            print("Invalid input. Please enter a positive integer.")


# from num1 to num2, find the maximum cycle length
def max_cycle_length(num1, num2):
    max = 0
    if num1 > num2:
        num1, num2 = num2, num1

    for i in range(num1, num2 + 1):
        if max < len(three_n_plus_one(i, [])):
            max = len(three_n_plus_one(i, []))
    return max


nums = get_user_input()

print(max_cycle_length(nums[0], nums[1]))
