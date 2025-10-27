import pytest
from app.calculations import add, sub, multiply, divide, BankAccount, InsufficientFundsException

@pytest.fixture
def zero_bank_account():
    print("Creating empty bank account")
    return BankAccount()

@pytest.fixture
def bank_account():
    print("Creating Bank Account with 50 Balance")
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected",[
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16),
])
def test_add(num1, num2, expected):
    print("Testing add function")
    assert add(num1, num2) == expected

def test_subtract():
    assert sub(9, 4) == 5


def test_multiply():
    assert multiply(4, 3) == 12


def test_divide():
    assert divide(20, 5) == 4

def test_bank_set_initial_amount(bank_account):
    print("Testing Bank Account with non-zero balance")
    assert bank_account.balance == 50

def test_bank_default_initial_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_account_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70

def test_account_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

@pytest.mark.parametrize("deposits, withdrawals, expected",[
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000),
])
def test_account_transactions(zero_bank_account, deposits, withdrawals, expected):
    zero_bank_account.deposit(deposits)
    zero_bank_account.withdraw(withdrawals)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFundsException):
        bank_account.withdraw(200)