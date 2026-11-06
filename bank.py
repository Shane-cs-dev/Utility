from abc import ABC, abstractmethod
import random, string
from typing import Optional

"""
Class Transactions
- This is for log generation purpose, so it would need teller_id and account_id. 
Probably amount for withdrawal and Deposit
- Argument: account_id, teller_id, (amount)
"""
class Transactions(ABC):
    def __init__(self, account_id, teller_id):
        self._account_id = account_id
        self._teller_id = teller_id
        
    @property
    def account_id(self):
        return self._account_id
    @property
    def teller_id(self):
        return self._teller_id

    # Define an abstract function to print the transaction
    @abstractmethod
    def transaction_description(self):
        pass

class Deposit(Transactions):
    def __init__(self, account_id, teller_id, amount):
        super().__init__(account_id, teller_id)
        self._amount = amount
    
    def transaction_description(self):
        return f"{self.teller_id} deposited {self._amount} to account {self.account_id}"
   
class Withdrawal(Transactions):
    def __init__(self, account_id, teller_id, amount):
        super().__init__(account_id, teller_id)
        self._amount = amount
        
    def transaction_description(self):
        return f"{self.teller_id} withdrew {self._amount} from account {self.account_id}"

class OpenAccount(Transactions):
    def __init__(self, account_id, teller_id, amount: int = 0):
        super().__init__(account_id, teller_id)
        self._balance = amount
    
    def transaction_description(self):
        return f"{self.teller_id} opened account, account id: {self.account_id}. Current balance is {self._balance}"

"""
Class Teller
- Need Teller_id and track their salary
- Arguments: teller_id, salary
"""
class Teller():
    def __init__(self, teller_id, salary):
        self._teller_id = teller_id
        self._salary = salary
    
    @property
    def salary(self):
        return self._salary
    @property
    def teller_id(self):
        return self._teller_id

"""
Class BankAccount
- Need the information of customer's name and a unique account_id, and the amount of money
they have in their account
- Argument: customer_name, account_id, balance
"""
class BankAccount():
    def __init__(self, customer_id, account_id, balance):
        self._customer_id = customer_id
        self._account_id = account_id
        self._balance = balance
    
    @property
    def balance(self):
        return self._balance
    
    def deposit(self, amount):
        print(f"{self._customer_id} deposited {amount} to account {self._account_id}")
        self._balance += amount
    def withdrawal(self, amount):
        print(f"{self._customer_id} withdrew {amount} from account {self._account_id}")
        self._balance -= amount
"""
Class Customer
"""
class Customer():
    def __init__(self, customer_name, account_id=None):
        self._customer_name = customer_name
        self._accounts_id = account_id if account_id else []
    
    def get_customer_name(self):
        return self._customer_name

    def get_accounts_id(self):
        return self._accounts_id

"""
Class BankSystem
- Map a unique customer_id to the BankAccount
"""
class BankSystem():
    def __init__(self):
        self._accounts = {} # account_id to BankAccount
        self._transactions = {
            "Open Account": [], 
            "Deposit": [], 
            "Withdrawal": [], 
            "Register Customer": []
        }
        self._customers = {} # customer_id to Customer
        
    # Define getter
    def get_accounts(self):
        return self._accounts
    def get_transactions(self):
        return self._transactions
    
    def register_customer(self, customer_name) -> str:
        while True:
            customer_id_format = string.ascii_uppercase + string.digits
            customer_id = 'C' + "".join(random.choices(customer_id_format, k = 12))
            if customer_id not in self._customers:
                # Add the customer to the self._customers
                self._customers[customer_id] = Customer(customer_name)
                return customer_id
            
    def generate_account_id(self):
        while True:
            account_format = string.ascii_uppercase + string.digits
            account_id = "ACCOUNT" + "".join(random.choices(account_format, k=20))
            if account_id not in self._accounts:
                return account_id
            
    def check_input_val(self, customer_id, amount):
        if amount <= 0:
            raise ValueError("User cannot open account with negative or 0 amount of money")
        if customer_id not in self._customers:
            raise ValueError(f"{customer_id} does not exist in the BankSystem. Please register before opening an account")
    
    def open_account(self, customer_id, amount, teller_id):
        self.check_input_val(customer_id, amount)
        
        # Generate an account_id and add this account_id to the BankSystem
        account_id = self.generate_account_id()
        self._accounts[account_id] = BankAccount(customer_id, account_id, amount) # Add account_id to the BankSystem
        self._customers[customer_id].get_accounts_id().append(account_id)
        
        # Update into transaction
        transact = OpenAccount(account_id, teller_id, amount)
        self._transactions["Open Account"].append(transact)
        print(f"Successfully opened account for customer {customer_id} and the account_id is {account_id}.")
        print(f"Current balance for this account: {self._accounts[account_id].balance}")
        return account_id
        
    def select_account(self, customer_id):
        customer = self._customers[customer_id]
        if len(customer.get_accounts_id()) == 1:
            return customer.get_accounts_id()[0]
        elif not customer.get_accounts_id():
            raise ValueError(f"{customer_id} hasn't opened account yet")
        
        for idx, account in enumerate(customer.get_accounts_id()):
            print(f"{idx + 1}: {account}")
        while True:
            account_num = input(f"Select the number of your account_id: ")
            if account_num.isdigit() and 1 <= int(account_num) <= len(customer.get_accounts_id()):
                return customer.get_accounts_id()[int(account_num) - 1]
    
    def deposit(self, customer_id, teller_id, amount, account_id=None):
        self.check_input_val(customer_id, amount)
        
        # If the user forgets their account_id
        if not account_id:
            account_id = self.select_account(customer_id)
        
        if account_id not in self._accounts:
            raise ValueError(f"{account_id} does not exist in the BankSystem")
        
        # Update the bank account
        account = self._accounts[account_id]
        account.deposit(amount)
        
        # Update the transaction
        transact = Deposit(account_id, teller_id, amount)
        self._transactions["Deposit"].append(transact)
        
    def withdrawal(self, customer_id, teller_id, amount, account_id=None):
        self.check_input_val(customer_id, amount)
        
        # If the user forgets their account_id
        if not account_id:
            account_id = self.select_account(customer_id)
        if account_id not in self._accounts:
            raise ValueError(f"{account_id} does not exist in the BankSystem")
        
        # Update the bank account
        account = self._accounts[account_id]
        if account.balance < amount:
            raise ValueError(f"{account_id} has no enough money")

        account.withdrawal(amount)
        
        # Update the transacetion
        transact = Withdrawal(account_id, teller_id, amount)
        self._transactions["Withdrawal"].append(transact)
        
        
        
        
        
        
        
        
        
    
    
