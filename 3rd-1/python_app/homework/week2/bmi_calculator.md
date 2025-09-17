# BMI 計算器解題思維

## 輸入處理

需要獲取體重和身高兩個數值，因為要獲取兩個數值，所以將獲取輸入的步驟寫成一個 `get_user_input` 函數，並處理數值轉換的問題

```python
def get_user_input(placeholder: str) -> float:
    num = 0
    while True:
        user_input = input(placeholder)
        try:
            num = float(user_input)
            if num > 0:
                return num
        except:
            pass
        print("輸入不正確，請重新輸入")

```

## BMI 計算

建立 `bmi_cal` 函數計算 BMI 值
- 將身高從公分轉為公尺 (除以 100)
- 套用公式: 體重 / 身高^2

## 健康狀態判斷

因為我真的不想寫那麼多 if, 所以設定閾值陣列 `[18.5, 25, 30, inf]`, 對應判斷結果 `["體重不足", "正常", "過重", "肥胖"]`然後用迴圈找出 BMI 落在哪個區間

```python
def get_bmi_judge(bmi: float) -> str:
    bmi_threshold = [18.5, 25, 30, float('inf')]
    bmi_judge = ["體重不足", "正常", "過重", "肥胖"]
    for i in range(len(bmi_threshold)):
        if bmi < bmi_threshold[i]:
            return bmi_judge[i]
```

## 輸出

最後將計算結果和判斷一起輸出給使用者
