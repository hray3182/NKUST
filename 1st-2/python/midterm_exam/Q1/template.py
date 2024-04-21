def table(a, b, c, d):
    for i in range(a, c+1):
        for j in range(1, 10):
            if i == a and j < b:
                continue
            if i >= c and j > d:
                break
            print(f"{i} x {j} = {i*j}\t", end=" ")
        print()

table(2,2,5,5)