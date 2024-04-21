from Item import Item
class Character:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.backpack = []
    
    def move_left(self):
        self.x-= 1
        print(f"{self.name} move to left")
    
    def move_right(self):
        self.x += 1
        print(f"{self.name} move to right")

    def move_up(self):
        self.y += 1
        print(f"{self.name} move to up")
    
    def move_down(self):
        self.y -= 1
        print(f"{self.name} move to down")

    def move(self, x, y):
        if x < 0:
            for i in range(abs(x)):
                self.move_left()
        if x > 0:
            for i in range(x):
                self.move_right()
        if y > 0:
            for i in range(y):
                self.move_up()
        if y < 0:
            for i in range(abs(y)):
                self.move_down()

    def pick_item(self, item: Item):
        if self.x == item.x and self.y == item.y:
            self.backpack.append(item)
            print(f"{self.name} pick up {item.name}")

    def __str__(self):
        return f"name: {self.name} position:{self.x}, {self.y}"
        