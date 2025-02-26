"""
ref: https://medium.com/swlh/atm-an-object-oriented-design-e3a2435a0830

objects:
- Bank
- ATM
- Account: 1 user must have 1 account
- Card: debt card, use card to login, access account
- Transaction

workflow
- user inserts card
- ATM verifies pin
- user can view balance, deposit, withdraw, and transfer
- user performs transaction
- ATM displays transaction details

""" 
from enum import Enum


class AccountState(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    CLOSED = "closed"  

class Card:
    def __init__(self, card_number, pin, account):
        self._card_number = card_number
        self._pin = pin
        self._account = account 

    @property
    def account(self):
        return self._account          

class Account:
    def __init__(self, account_id, amount):
        self._account_id = account_id
        self._balance = amount
        self._cards = []
        self._state = AccountState.INACTIVE
    
    @property
    def account_id(self):
        return self._account_id
    
    @property
    def balance(self):
        return self._balance
    
    @property
    def cards(self):
        return self._cards
    
    @property
    def state(self):
        return self._state
    
    def add_card(self, card):
        self._cards.append(card)

    def remove_card(self, card):
        if card in self._cards:
            self._cards.remove(card)
        else:
            raise Exception("Card not found in Account")
   
    def increase_balance(self, amount):
        self._balance += amount

    def decrease_balance(self, amount):
        self._balance -= amount   


class ATM:
    def __init__(self, atm_id, location):
        self._atm_id = atm_id
        self._location = location
        self._current_card = None
        self._current_account = None
    
    @property
    def current_card(self):
        return self._current_card
    
    @property
    def current_account(self):
        return self._current_account
       
    def login(self, card, entered_pin):
        if card.pin == entered_pin:
            self._current_card = card
            account = card.account
            self._current_account = account
            account.state = AccountState.ACTIVE
        else:
            raise Exception("Invalid PIN")
        
    def view_balance(self, account):
        if account.state == AccountState.ACTIVE:
            return f"Balance: {account.balance}"
        else:
            raise Exception("Account Not Logged In")
    
    def deposit(self, account, amount):
        if account.state == AccountState.ACTIVE:
            account.increase_balance(amount)
            return f"Deposit successful, new balance: {account.balance}"
        else:
            raise Exception("Account Not Logged In")
    
    def withdraw(self, account, amount):
        if account.state == AccountState.ACTIVE:
            # check if amount is more than balance
            if amount > account.balance:
                raise Exception("Insufficient balance")
            account.decrease_balance(amount)
            return f"Withdrawal successful, new balance: {account.balance}"
        else:
            raise Exception("Account Not Logged In")
    
    
    def transfer(self, account, amount, recipient):
        if account.state == AccountState.ACTIVE:
            # check if amount is more than balance
            if amount > account.balance:
                raise Exception("Insufficient balance")
            account.decrease_balance(amount)
            recipient.increase_balance(amount)
            return f"Transfer successful, new balance: {account.balance}"
        else:
            raise Exception("Account Not Logged In")
        
    
    
    