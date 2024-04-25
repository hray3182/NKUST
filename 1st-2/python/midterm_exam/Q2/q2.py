import Module as m

def div():
    print("-"*20)

ray = m.Customer("E123456789", "Ray", "0900123456")
kesha = m.Customer("E223456789", "Kesha", "0907456123")
dog = m.Customer("E112544987", "Ming", "0914579654")

div()
single = m.SingleRoom(501)
print(single)
div()
double = m.DoubleRoom(502)
print(double)
div()

single.book(dog)
div()
double.book(ray)

div()
single.add_resident(dog)
div()
# 嘗試再多加一位住戶到單人房
single.add_resident(ray)
div()
double.add_resident(ray)
div()
double.add_resident(kesha)
div()
# 嘗試再多加一位住戶到雙人房
double.add_resident(dog)

hotel = m.Hotel("帝國大飯店")
hotel.add_room(single)
hotel.add_room(double)
hotel.add_room(m.SingleRoom(503))
hotel.add_room(m.SingleRoom(504))
hotel.add_room(m.SingleRoom(505))
hotel.add_room(m.SingleRoom(506))
hotel.add_room(m.SingleRoom(507))
hotel.add_room(m.SingleRoom(508))

hotel.list_rooms()
