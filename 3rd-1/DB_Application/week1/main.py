import math 

def main():
    x1, y1 = 0, 0
    x2, y2 = -30, 60
    x3, y3 = 30, 60

    a = math.sqrt((x2 - x3) * (x2 - x3) + (y2 - y3) * (y2 - y3))
    b = math.sqrt((x1 - x3) * (x1 - x3) + (y1 - y3) * (y1 - y3))
    c = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
    A = math.degrees(math.acos((a * a - b * b - c * c) / (-2 * b * c)))
    B = math.degrees(math.acos((b * b - a * a - c * c) / (-2 * a * c)))
    C = math.degrees(math.acos((c * c - b * b - a * a) / (-2 * a * b)))
    #輸出結果
    print("The three angles are ", round(A * 100) / 100.0, round(B * 100) / 100.0, round(C * 100) / 100.0)


if __name__ == "__main__":
    main()
