def idiot_code_generator(max_i, max_j):
    output = []
    identation = "    "
    f = open("table_generator.py", "w")
    f.write("def table(a, b, c, d):\n")
    count_if = 0
    for a in range(1, max_i + 1):  
        for b in range(1, max_j + 1):  
            for c in range(a, max_i + 1): 
                for d in range(1, max_j + 1):  
                    condition = f"{identation}if a == {a} and b == {b} and c == {c} and d == {d}:"
                    calculations = []
                    for i in range(a, c + 1):
                        currentRow = []
                        for j in range(1, max_j + 1):
                            if i == a and j < b:
                                continue
                            if i >= c and j > d:
                                break
                            currentRow.append(f"{i} x {j} = {i*j}")
                        if currentRow:
                            s = "\\t".join(currentRow)
                            calculations.append(f"{identation*2}print(\"{s}\")\n")
                    if calculations:
                        output.append(condition)
                        output.append("".join(calculations))
                        count_if +=1
    f.write("\n".join(output))
    f.close()
    print(count_if)

max_i = 30
idiot_code_generator(9,9)
