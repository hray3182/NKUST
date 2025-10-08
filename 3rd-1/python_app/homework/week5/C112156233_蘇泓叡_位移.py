slice = [i for i in range(10)]
for i in range(10):
    slice = slice[1:] + slice[0:1]
    print(slice)
