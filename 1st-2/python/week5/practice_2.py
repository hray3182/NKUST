class book:
    def __init__(self, name, author, isbn):
        self.name = name
        self.author = author
        self.isbn = isbn 

    def get_title(self):
        return self.name

    def get_author(self):
        return self.author

    def get_isbn(self):
        return self.isbn

class record:
    def __init__(self, user, book, action):
        # action 0 為借, 1 為還
        self.user = user
        self.book = book
        self.action = action


class user:
    def __init__(self, name, records):
        self.name = name
        self.records = records

    def borrow_book(self, book):
        self.records.append(record(self, book, 0))
        print(f"{self.name} 借了 {book.get_title()}")

    def return_book(self, book):
        self.records.append(record(self, book, 1))
        print(f"{self.name} 還了 {book.get_title()}")

    def print_records(self):
        for record in self.records:
            print(f"{self.name} {record.action} {record.book.get_title()}")

# def some books 
book1 = book("Python Programming", "John", "123456")
book2 = book("Java Programming", "Tom", "654321")
book3 = book("C Programming", "Peter", "456789")

# def user
user1 = user("Ray", [])

# borrow a book
user1.borrow_book(book1)

# return a book
user1.return_book(book1)

print("借書記錄: ")
user1.print_records()