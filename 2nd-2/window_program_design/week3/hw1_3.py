def print_table():
    for i in range(1, 9):
        for j in range(2, 6):
            print(f"{j} * {i} = {i*j}", end="\t")
        print()

    for i in range(1, 9):
        for j in range(6, 10):
            print(f"{j} * {i} = {i*j}", end="\t")
        print()

if __name__ == "__main__":
    print_table()


