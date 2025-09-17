def is_leap_year(year: int):
    return (year % 4 == 0 and not year % 100 == 0) or year % 400 == 0

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

# print(f"{year}年{is_leap_year(year)? "是":"不是"}閏年")
print(f"{year}年{'是' if is_leap_year(year) else '不是'}閏年")

