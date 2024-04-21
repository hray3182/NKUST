from Item import Item
from Chracter import Character
import random
class Map:
    def __init__(self, size_x, size_y) -> None:
        self.size_x = size_x
        self.size_y = size_y
        self.items : list[Item] = []
        self.chracter: Character = None
    
    def add_item(self, item: Item):
        self.items.append(item)

    def remove_item(self, item:Item):
        self.items.remove(item)

    def add_chracter(self, chracter: Character):
        self.chracter = chracter

    def chracter_move_left(self):
        if self.chracter.x:
            return
        self.chracter.move_left()
    
    def chracter_move_right(self):
        if self.chracter.x == self.size_x:
            return
        self.chracter.move_right()
    
    def chracter_move_up(self):
        if self.chracter.y == self.size_y:
            return
        self.chracter.move_up()

    def chracter_move_down(self):
        if self.chracter.y:
            return
        self.chracter.move_down()

    def random_move(self):
        rand = random.randint(0, 3)
        if rand == 0:
            self.chracter_move_down()
        if rand == 1:
            self.chracter_move_left()
        if rand == 2:
            self.chracter_move_right()
        if rand == 3:
            self.chracter_move_up()