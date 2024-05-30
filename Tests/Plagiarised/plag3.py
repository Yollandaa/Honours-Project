class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance  # Private attribute

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Added {amount} to the balance")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.__balance:
            self.__balance -= amount
            print(f"Withdrew {amount} from the balance")
        else:
            print("Insufficient funds or invalid amount")

    def get_balance(self):
        return self.__balance


# Create an instance
account = BankAccount("John")

# Use the methods to interact with the private attribute
account.deposit(1000)
account.withdraw(500)
print(account.get_balance())  # Output: 500
