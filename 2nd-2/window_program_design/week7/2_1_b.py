import tkinter as tk
root = tk.Tk()
root.title("2-2")
width = 600
height = 200
root.geometry(f"{width}x{height}")

gap = 10
object_count = 5
object_width = (width - 2* gap * (object_count - 1)) / object_count

start_x = gap
start_y = gap

canvas = tk.Canvas(root, width=width, height=height)
canvas.pack()
canvas.create_rectangle(0, 0, width, height, fill="gray")

class exclamation_mark:
    def __init__(self, canvas, x, y, width=150, height=150, fill="black", outline="black", border_width=2, dash=()):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fill = fill
        self.outline = outline
        self.border_width = border_width
        self.dash = dash
        self.oval_height = height * 0.7
        self.circle_radius = width * 0.2

    def draw(self):
        # 橢圓（驚嘆號的上半部分）
        oval_width = self.width * 0.4  
        oval_x = self.x + (self.width - oval_width) / 2
        self.canvas.create_oval(
            oval_x,
            self.y,
            oval_x + oval_width,
            self.y + self.oval_height,
            fill=self.fill,
            outline=self.outline,
            width=self.border_width,
            dash=self.dash
        )
        
        # 圓形（驚嘆號的下半部分）
        circle_radius = self.width * 0.2  
        circle_y_offset = self.oval_height +  10 
        self.canvas.create_oval(
            self.x + self.width/2 - circle_radius,
            self.y + circle_y_offset,
            self.x + self.width/2 + circle_radius,
            self.y + circle_y_offset + circle_radius * 2,
            fill=self.fill,
            outline=self.outline,
            width=self.border_width,
            dash=self.dash
        )

color_schemes = [
    {"fill": "gray", "outline": "black", "border_width": 1, "dash": ()},
    {"fill": "gray", "outline": "black", "border_width": 5, "dash": ()},
    {"fill": "red", "outline": "black", "border_width": 5, "dash": ()},
    {"fill": "red", "outline": "blue", "border_width": 5, "dash": ()},
    {"fill": "white", "outline": "green", "border_width": 2, "dash": (5, 5)}
]

for i in range(object_count):
    mark = exclamation_mark(
        canvas,
        start_x,
        start_y,
        object_width,
        150,
        color_schemes[i]["fill"],
        color_schemes[i]["outline"],
        color_schemes[i]["border_width"],
        color_schemes[i]["dash"]
    )
    mark.draw()
    start_x += object_width + gap

root.mainloop()

