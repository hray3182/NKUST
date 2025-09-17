sets = [[1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31],
 [2,3,6,7,10,11,14,15,18,19,22,23,26,27,30,13],
 [4,5,6,7,12,13,14,15,20,21,22,23,28,29,30,31],
 [8,9,10,11,12,13,14,15,24,25,26,27,28,29,30,31],
 [16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]]

def print_set(arr):
    for i in range(1, len(arr)+1):
        print(f"{arr[i-1]:2d}", end=" ")
        if (i) % 4 == 0:
            print()

# main function
anwser = 0

valid_inputs = ["y", "Y", "n", "N"]

for i in range(5):

    valid_input = False

    # loop until valid input
    while not valid_input:
        print("你的生日日期有在下面出現嗎(y/n)")

        print_set(sets[i])

        user_input = input(":")

        if user_input not in valid_inputs:
            print("無效輸入，請重新輸入")
            continue
        # if true, add the first element in current set to anwser
        if user_input == "y" or user_input == "Y":
            anwser += sets[i][0]
            valid_input=True
        # if false, skip
        if user_input == "n" or user_input == "N":
            valid_input = True

print("----------------------------")
print(f"你的生日為{anwser}")
