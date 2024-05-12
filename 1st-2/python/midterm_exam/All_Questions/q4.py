class Account_A:
    def __init__(self, id, name, balance) -> None:
        self.id = id
        self.name = name
        self.balance = balance

    def __str__(self) -> str:
        return f"ID: {self.id}, Name: {self.name}, Balance: {self.balance}"

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposit: {amount}")
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient balance"
        else:
            self.balance -= amount
            print(f"Withdraw: {amount}")
            return self.balance

    def get_balance(self):
        return self.balance

    
class CheckingAccount(Account_A):
    def __init__(self, id, name, balance, limit) -> None:
        super().__init__(id, name, balance)
        self.transactions_limit =  limit
        self.transactions = 0

    def withdraw(self, amount):
        if self.transactions >= self.transactions_limit:
            return "Transaction limit reached"
        else:
            self.transactions += 1
            return super().withdraw(amount)
    
    def deposit(self, amount):
        if self.transactions >= self.transactions_limit:
            return "Transaction limit reached"
        else:
            self.transactions += 1
            return super().deposit(amount) 
    
    def reset_transactions(self):
        self.transactions = 0

class SavingsAccount(Account_A):
    def __init__(self, id, name, balance) -> None:
        super().__init__(id, name, balance)
        self.record = []
        
    def deposit(self, amount):
        self.record.append(amount)
        return super().deposit(amount)

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient balance"
        else:
            self.record.append(-amount)
            return super().withdraw(amount)

    def print_history(self):
        for i in self.record:
            print(i)
            
if __name__ == "__main__":
    a = Account_A(1, "John", 1000)
    print(a)
    
    a.deposit(2000)
    print(a)
    a.withdraw(500)
    print(a)
    
    c = CheckingAccount(2, "Alice", 2000, 3)
    print(c)
    
    c.deposit(500)
    print(c)
    c.withdraw(200)
    print(c)
    c.withdraw(200)
    print(c)
    c.withdraw(200)
    print(c)
    
    c.reset_transactions()
    c.withdraw(200)
    
    s = SavingsAccount(3, "Bob", 3000)
    print(s)
    
    s.deposit(1000)
    print(s)
    s.withdraw(500)
    print(s)
    s.withdraw(2000)
    print(s) 

    s.print_history()
