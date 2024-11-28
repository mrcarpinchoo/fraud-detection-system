# core modules
import os

# third-party modules
import requests

def signUp():
    print("Sign Up")

    name = input("Enter your name: ")
    email = input("Enter your email: ")
    accounts = []

    customer = {
        "name": name,
        "email": email,
        "accounts": accounts
    }

    # request
    suffix = "/customers"

    endpoint = f"{API_URL}{suffix}"

    res = requests.post(endpoint, json = customer)

    if not res.ok: print(f"Failed to post customer: {res.json()}")
    else: print(f"Customer created successfully! {customer}")
# end def

def getCustomerByEmail(email):
    # request
    suffix = f"/customers/{email}"

    endpoint = f"{API_URL}{suffix}"

    res = requests.get(endpoint)

    if not res.ok:
        print(f"Failed to retrieve customer {email}: {res.json()}")
        return None
    # end def
    
    return res.json()
# end def

def createAccount(customerEmail):
    print("Create New Account")

    customer = getCustomerByEmail(customerEmail)

    # request
    suffix = f"/customers/{customer['_id']}/accounts"

    endpoint = f"{API_URL}{suffix}"

    res = requests.put(endpoint, json = {})

    if not res.ok: print(f"Failed to post account: {res.json()}")
    else: print(f"Account created successfully! {res.json()}")
# end def

def printCustomerAccounts(accounts):
    for i, account in enumerate(accounts, start = 1):
        print("{:2d} Account {:<16} | Balance: ${:>9.2f}; Expiration date: {}".format(i, account["number"], account["balance"], account["expiration_date"]))
# end def

def retrieveCustomerInformation(customerEmail):
    print("Retrieve Customer Information")

    print()

    customer = getCustomerByEmail(customerEmail)

    print(f"{'Customer:'.ljust(10)} {customer['name']}")
    print(f"{'Email:'.ljust(10)} {customer['email']}")

    print()

    printCustomerAccounts(customer["accounts"])

    print()
# end def

def printTransactionMenu():
    options = {
        0: "Back",
        1: "Deposit",
        2: "Withdrawal",
        3: "Transference"
    }

    for key in options.keys(): print(f"{key}. {options[key]}")

    print()
# end def

def performDeposit(customerEmail):
    print("Perform Deposit")

    print()

    customer = getCustomerByEmail(customerEmail)

    accounts = customer["accounts"]

    print("Select the account to perform the transaction:")

    printCustomerAccounts(accounts)

    opt = int(input("Enter your choice: "))

    print()

    amount = float(input("Enter the amount to deposit: ").strip() or 0)

    if amount <= 0: # checks whether the amount is greater than 0
        input("The amount to deposit must be greater than 0. Press \"enter\" to cotinue...")
        return
    # end if

    accountNumber = accounts[opt - 1]["number"]

    details = {}

    transaction = {
        "customer_email": customerEmail,
        "account_number": accountNumber,
        "transactionType": "deposit",
        "amount": amount,
        "details": details 
    }

    # request
    suffix = f"/transactions"

    endpoint = f"{API_URL}{suffix}"

    res = requests.post(endpoint, json = transaction)

    if not res.ok: print(f"Failed to perform transaction: {res.json()}")
    else: print(f"Transaction performed successfully! {transaction}")
# end def

def performWithdrawal(customerEmail):
    pass
# end def

def performTransfer(customerEmail):
    pass
# end def

def performTransaction(customerEmail):
    while (True):
        print("Perform Transaction")

        print()

        printTransactionMenu()

        opt = int(input("Enter your choice: "))

        if opt == 0: return
        elif opt == 1: performDeposit(customerEmail)
        elif opt == 2: performWithdrawal(customerEmail)
        elif opt == 3: performTransfer(customerEmail)
        # end if-elif
    # end def
# end def

# environment variables
API_URL = os.getenv("API_URL", "http://localhost:8000/api")