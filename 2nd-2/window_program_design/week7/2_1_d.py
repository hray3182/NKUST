import tkinter as tk

root = tk.Tk()
root.title("2_1_d")

canvas_width = 400
canvas_height = 400

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

image = tk.PhotoImage(file="2_1_d.png")
canvas.create_image(0, 0, image=image, anchor="nw")

root.mainloop()



