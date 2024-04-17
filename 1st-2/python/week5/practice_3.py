class product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def get_name(self):
        return self.name
    
    def get_price(self):
        return self.price
    
    def get_stock(self):
        return self.stock
    
    def add_stock(self, quantity):
        self.stock += quantity

    def minus_stock(self, quantity):
        self.stock -= quantity
    
    def __str__(self):
        return f"品名: {self.name}\t價格: {self.price} \t庫存: {self.stock}"


class cartItem:
    def __init__(self, product: product, quantity):
        self.product = product
        self.quantity = quantity

class carts:
    def __init__(self):
        self.items = []
    
    def add_item(self, item: cartItem):
        self.items.append(item)
    
    def remove_item(self, item: cartItem):
        for i in range(len(self.items)):
            if self.items[i].product.get_name() == item.product.get_name():
                self.items.pop(i)
                break
        
    def get_total(self):
        total = 0
        for item in self.items:
            total += item.product.get_price() * item.quantity
        return total

    def show_items(self):
        for item in self.items:
            print(f"品名: {item.product.get_name()}, 數量: {item.quantity}, 單價: {item.product.get_price()}")

    def checkout(self):
        print(f"總價: {self.get_total()}")
        for item in self.items:
            item.product.minus_stock(item.quantity)
        self.items = []

class user:
    def __init__(self, name, carts: carts):
        self.name = name
        self.carts = carts

    def add_product(self, product, quantity):
        print(f"{self.name} 將 {quantity} 個 {product.get_name()} 放入購物車")
        if product.get_stock() < quantity:
            print(f"{product.get_name()} 庫存不足")
            return
        for i in range(len(self.carts.items)):
            if self.carts.items[i].product.get_name() == product.get_name():
                self.carts.items[i].quantity += quantity
                return
        self.carts.add_item(cartItem(product, quantity))


    def remove_product(self, product, quantity):
        for i in range(len(self.carts.items)):
            if self.carts.items[i].product.get_name() == product.get_name():
                if self.carts.items[i].quantity < quantity:
                    print(f"{product.get_name()} 購物車內數量不足")
                    return
                self.carts.items[i].quantity -= quantity
                if self.carts.items[i].quantity == 0:
                    self.carts.remove_item(cartItem(product, quantity))

        print(f"{self.name} 將 {quantity} 個 {product.get_name()} 移出購物車")

def print_divider(n):
    print("-"*n)

# def some product 
apple = product("Apple", 10, 100)
banana = product("Banana", 5, 200)
orange = product("Orange", 15, 50)
print("新增商品", apple)
print("新增商品", banana)
print("新增商品", orange)

print_divider(20)

# def a user
user1 = user("Ray", carts())

# Ray add some product to cart
user1.add_product(apple, 10)
user1.add_product(banana, 20)
user1.add_product(orange, 5)
print_divider(20)
print("嘗試用超過目前庫存數量將商品加入購物車")
# try to add more than stock quantity
user1.add_product(apple, 200)

print_divider(20)
# Ray remove some product from cart
user1.remove_product(apple, 5)

print_divider(20)
# Ray want to know what he buy
user1.carts.show_items()

print_divider(20)
# Ray go to checkout
user1.carts.checkout()
print_divider(20)

# print product stock
print("查看商品目前庫存")
print(apple)
print(banana)
print(orange)

