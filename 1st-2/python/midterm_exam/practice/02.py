from Item import Item
from Chracter import Character

key = Item("key", 1,1)
byron = Character("Byron", 0, 0)

byron.move(1,1)
byron.pick_item(key)