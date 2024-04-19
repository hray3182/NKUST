class Rooms:
    def __init__(self, id , model, price):
        self.id = id
        self.model = model
        self.price = price
        self.booked:bool = False

    def __str__(self):
        s = f"房號 {self.id} \n房型: {self.model} \n每晚價格: {self.price} \n是否被預約: {self.is_book()}"
        return s
    
    def book(self, customer: 'Customer'):
        self.booked = True
        print(f"{customer} 預定 {self}")

    def unbook(self):
        if not self.booked:
            print(f"{self} 尚未被預訂，無法取消")
            return
        print(f"已取消{self}的預定")
        self.booked = False
    
    def is_book(self):
        if self.booked:
            return "是"
        return "否"

class Customer:
    def __init__(self, id, name, phone):
        self.name = name
        self.phone = phone
        self.id = id
    
    def __str__(self):
        return self.name
        

class SingleRoom(Rooms):
    def __init__(self, id):
        super().__init__(id, "Single Room", 1800)
        self.resident = None
    
    def add_resident(self, customer: Customer):
        if not self.resident == None:
            print("單人房僅能有一位住戶")
            return
        self.resident = customer
        print(f"{customer} 入住 {self}")

    def remove_resident(self):
        if not self.resident == None:
            print("目前已無住戶")
            return
        print(f"{self.resident} 搬離 {self}")
        self.resident = None

class DoubleRoom(Rooms):
    def __init__(self, id):
        super().__init__(id, "Double Room", 2800)
        self.residents = []
    
    def add_resident(self, customer: Customer):
        if len(self.residents) == 2:
            print("雙人最多只能有2位住戶")
            return
        self.residents.append(customer)
        print(f"{customer} 入住 {self}")

    def remove_resident(self):
        if len(self.residents) == 0:
            print("目前已無住戶")
            return
        for resident in self.residents:
            print(f"{resident} 搬離 {self}")
        self.residents = []

class Hotel:
    def __init__(self, name):
        self.name = name
        self.rooms =[]
    
    def __str__(self):
        return self.name

    def list_rooms(self):
        for room in self.rooms:
            print(f"房號: {room.id}\t房型: {room.model}\t 是否被預訂:{room.is_book()}")

    def add_room(self, room):
        self.rooms.append(room)