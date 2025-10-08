def get_nums():
    num_arrs = []
    while True:
        try:
            nums_str = input("請輸入10個1~99範圍內的數字，並用 space 隔開： ")
            str_arr = nums_str.split(" ")
            if str_arr[0] == "0":
                return num_arrs
            num_arr = []
            for i in range(len(str_arr)):
                number = int(str_arr[i])
                num_arr.append(number)
            if len(num_arr) == 10:
                num_arrs.append(num_arr)
            else:
                print("請輸入10個數字")
        except:
            print("輸入不正確，請重新輸入")


def check_arrs(arrs):
    nums = []
    for i in range(len(arrs)):
        for j in range(10):
            nums.append(arrs[i][j])

    unix = set(nums)

    if len(unix) < 99:
        return False

    for i in range(1, 100):
        if i not in unix:
            return False

    return True


def test_check_arrs():
    # Test Case 1: 正常情況 - 包含 1-99 所有數字
    # 創建一個 10x10 的陣列,前 99 個位置填入 1-99,最後一個位置填 1
    arrs1 = []
    nums = list(range(1, 100))  # [1, 2, 3, ..., 99]
    nums.append(1)  # 湊滿 100 個數字

    for i in range(10):
        arrs1.append(nums[i * 10 : (i + 1) * 10])

    assert check_arrs(arrs1) == True, "應該返回 True,因為包含 1-99 所有數字"
    print("Test Case 1 通過!")

    # Test Case 2: 缺少某個數字 - 缺少數字 50
    # 創建一個 10x10 的陣列,用數字 1 替代 50
    arrs2 = []
    nums2 = list(range(1, 50)) + [1] + list(range(51, 100))  # 用 1 替代 50
    nums2.append(1)  # 湊滿 100 個數字

    for i in range(10):
        arrs2.append(nums2[i * 10 : (i + 1) * 10])

    assert check_arrs(arrs2) == False, "應該返回 False,因為缺少數字 50"
    print("Test Case 2 通過!")


# 執行測試
# test_check_arrs()


result = check_arrs(get_nums())
print(f"檢查結果: {'通過' if result else '失敗'}")
