class Book:
    def __init__(self, name, author) -> None:
        self.name = name
        self.author = author
        self.is_borrowed = False

class User:
    def __init__(self, name, id) -> None:
        self.name = (name)
        self.id = id
        self.borrowed_books = []
    
    def borrow_book(self, book: Book):
        if book.is_borrowed:
            print("Book is already borrowed")
        else:
            book.is_borrowed = True
            self.borrowed_books.append(book)
            print(f"{self.name} has borrowed {book.name}")

    def return_book(self, book: Book):
        if book in self.borrowed_books:
            book.is_borrowed = False
            self.borrowed_books.remove(book)
            print(f"{self.name} has returned {book.name}")
        else:
            print("You have not borrowed this book") 

class Staff(User):
    def __init__(self, name, id, staff_id) -> None:
        self.staff_id = staff_id
        super().__init__(name, id)

    def add_book(self, book_list: list, book: Book):
        book_list.append(book)
        print(f"{self.name} has added {book.name} to the library")

    def remove_book(self, book_list: list, book: Book):
        if book in book_list:
            book_list.remove(book)
            print(f"{self.name} has removed {book.name} from the library")
        else:
            print("Book is not in the library")


if __name__ == "__main__":
    book1 = Book("Book1", "Author1")
    book2 = Book("Book2", "Author2")
    book3 = Book("Book3", "Author3")
    book_list = [book1, book2, book3]

    user = User("User", 1)
    
    staff = Staff("Staff", 2, 1)

    user.borrow_book(book1)
    user.borrow_book(book2)

    # 嘗試借已經被借走的書
    user.borrow_book(book1)

    user.return_book(book1)

    new_book = Book("Book4", "Author4")

    staff.add_book(book_list, new_book)
    staff.remove_book(book_list, book2)

    # 嘗試刪除不存在的書
    staff.remove_book(book_list, book2)