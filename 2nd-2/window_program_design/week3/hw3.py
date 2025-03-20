def BMI_calculate(height, weight):
    return weight / (height / 100) ** 2

def BMI_category(BMI):
    if BMI < 18.5:
        return "過輕"
    elif BMI >= 18.5 and BMI < 24:
        return "正常"
    elif BMI >= 24 and BMI < 27:
        return "過重"
    else:
        return "肥胖"

if __name__ == "__main__":  
    height = float(input("請輸入身高(公分): "))
    weight = float(input("請輸入體重(公斤): "))
    BMI = BMI_calculate(height, weight)
    print(f"BMI: {BMI:.2f}")
    print(f"BMI 指數: {BMI_category(BMI)}")
