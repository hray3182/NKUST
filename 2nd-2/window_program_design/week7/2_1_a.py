import tkinter as tk
root = tk.Tk()
root.title("2-1")
root.geometry("800x402")

# 計算總寬度：5個矩形 + 4個間距
canvas = tk.Canvas(root, width=800, height=400, bg="gray")
canvas.pack()


# first: color transparent, border black 2px
canvas.create_rectangle(10, 10, 60, 300, fill="gray", outline="black", width=2)

# second: color transparent, boarder black 10px
canvas.create_rectangle(70, 10, 120, 300, fill="white", outline="black", width=5)

# third: color rad, board black 10px
canvas.create_rectangle(130, 10, 180, 300, fill="red", outline="black", width=5)

# fourth: color red, board blue 10px
canvas.create_rectangle(190, 10, 240, 300, fill="red", outline="blue", width=5)

# fifth: color white, board green dash 4px
canvas.create_rectangle(250, 10, 300, 300, fill="gray", outline="green", width=4, dash=(10, 5))


root.mainloop()
