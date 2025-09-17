# 判斷是否為閏年解題思維

首先我需要一個函數判斷是否為閏年
```python
def is_leap_year(year: int):
    return (year % 4 == 0 and not year % 100 == 0) or year % 400 == 0
```

再來我需要獲取user input, 並處理數值轉換的問題，我用顯式轉換將`user_input`從 string 轉換成 int, 並用 try 語法捕捉例外，直到使用者輸入了正確數值才會進入下一階段

```python
year = 0
while True:
    user_input = input("請輸入年份: ")
    try:
        year = int(user_input)
        if year > 0:
            break
    except:
        pass
    print("輸入不正確，請重新輸入")
```

最後是輸出的部份，原本想要用三元判斷，不過有語法錯誤，後來問 ai 才知道 python 沒有三元判斷但是類似的語法
```python
# 錯誤的語法!!
print(f"{year}年{is_leap_year(year)? "是":"不是"}閏年")

# AI 給的
print(f"{year}年{'是' if is_leap_year(year) else '不是'}閏年")
```
