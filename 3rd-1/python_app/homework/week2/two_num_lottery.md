# 雙號彩券解題思維

## 輸入處理

需要獲取兩個不重複的 0-9 數字，建立 `get_user_input` 函數來處理輸入驗證：
- 確保輸入為有效整數
- 限制範圍在 0-9 之間
- 處理無效輸入並提示重新輸入

```python
def get_user_input(placeholder: str) -> int:
    num = 0
    while True:
        user_input = input(placeholder)
        try:
            num = int(user_input)
            if num >= 0 and num < 10:
                return num
        except:
            pass
        print("輸入不正確，請重新輸入")
```

## 防止重複數字

使用 while 迴圈確保兩個輸入數字不相同：
- 持續要求輸入直到獲得兩個不同的數字
- 若數字相同則提示使用者重新輸入

## 開獎機制

建立 `get_prize` 函數處理開獎邏輯：
- 使用 `random.sample` 從 0-9 中隨機抽取 2 個不重複數字作為中獎號碼
- 根據不同中獎條件返回對應獎金：
  1. 完全符合順序：$10,000
  2. 號碼相同但順序相反：$3,000
  3. 有一個數字符合：$1,000
  4. 都不符合：$0

```python
def get_prize(num1, num2) -> int:
    right = random.sample(range(9), 2)
    print(f"開獎號碼為{right[0]}, {right[1]}")
    if right[0] == num1 and right[1] == num2:
        return 10000
    if right[0] == num2 and right[1] == num1:
        return 3000
    if num1 in right or num2 in right:
        return 1000
    return 0
```

## 輸出

顯示開獎號碼和獲得的獎金給使用者