def add(num1: int, num2: int):
    """Returns the sum of two numbers."""
    return num1 + num2

def sub(num1: int, num2: int):
    """Returns the difference of two numbers."""
    return num1 - num2

def multiply(num1: int, num2: int):
    """Returns the multiplication of two numbers."""
    return num1 * num2

def divide(num1: int, num2: int):
    """Returns the division of two numbers."""
    return num1 / num2

class InsufficientFundsException(Exception):
    pass


class BankAccount():
    def __init__(self, starting_balance = 0):
        self.balance = starting_balance

    def __str__(self):
        return f"BankAccount balance: {self.balance}"
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsException("Insufficient Funds in the account")
        self.balance -= amount
    
    def collect_interest(self):
        self.balance *= 1.1