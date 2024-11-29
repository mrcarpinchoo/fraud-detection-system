# core modules
import os

# third-party modules
import requests

def signUp():
    print("Sign Up")

    customer_name = input("Enter your name: ")
    customer_email = input("Enter your email: ")

    customer = {
        "customer_name": customer_name,
        "customer_email": customer_email,
        "customer_accounts": []
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

def createAccount(customer_email):
    print("Create Account")

    customer = getCustomerByEmail(customer_email)

    if not customer: return # returns if customer was not retrieved

    account = { "customer_email": customer_email }

    # request
    suffix = f"/accounts"

    endpoint = f"{API_URL}{suffix}"

    res = requests.post(endpoint, json = account)

    if not res.ok: print(res.json())
    else: print(f"Account created successfully!\n{res.json()}")
# end def

def printCustomerAccounts(accounts):
    for i, account in enumerate(accounts, start = 1):
        print("{:2d} Account {:<16} | Balance: ${:>9.2f}; Expiration date: {}".format(i, account["account_number"], account["account_balance"], account["account_expiration_date"]))
# end def

def getAccountsByEmail(customer_email):
    # request
    suffix = f"/accounts?customer_email={customer_email}"

    endpoint = f"{API_URL}{suffix}"

    res = requests.get(endpoint)

    if not res.ok: return None
    # end def

    return res.json()
# end def

def retrieveCustomerInformation(customer_email):
    print("Retrieve Customer Information")

    print()

    customer = getCustomerByEmail(customer_email)

    if not customer: return # returns if customer was not retrieved

    print(f"{'Customer:'.ljust(10)} {customer['customer_name']}")
    print(f"{'Email:'.ljust(10)} {customer['customer_email']}")

    accounts = getAccountsByEmail(customer_email)

    print()

    if accounts != None: printCustomerAccounts(accounts)
    else: print(f"Customer with email {customer_email} has not yet created an account.")

    print()
# end def

def printTransactionMenu():
    options = {
        0: "Back",
        1: "Deposit",
        2: "Withdraw",
        3: "Transfer"
    }

    for key in options.keys(): print(f"{key}. {options[key]}")

    print()
# end def

def performTransactionRequest(transaction):
    # request
    suffix = f"/transactions"

    endpoint = f"{API_URL}{suffix}"

    return requests.post(endpoint, json = transaction)
# end def

def performDeposit(customer_email):
    print("Perform Deposit")

    print()

    print("Select the account to deposit:")

    print()

    accounts = getAccountsByEmail(customer_email)

    printCustomerAccounts(accounts)

    opt = int(input("Enter your choice: "))

    print()

    transaction_amount = float(input("Enter the amount to deposit: ").strip() or 0)

    if transaction_amount <= 0: # checks whether the amount is greater than 0
        input("The amount to deposit must be greater than 0. Press \"enter\" to cotinue...")
        return
    # end if

    account_number = accounts[opt - 1]["account_number"]

    transaction = {
        "customer_email": customer_email,
        "account_number": account_number,

        "transaction_type": "deposit",
        "transaction_amount": transaction_amount,
        "transaction_details": {} 
    }

    res = performTransactionRequest(transaction)

    if not res.ok: print(f"Failed to perform deposit: {res.json()}")
    else: print(f"Deposit performed successfully! {transaction}")
# end def

def printWithdrawalMethods():
    options = {
        1: "ATM",
        2: "cashier",
    }

    for key in options.keys(): print(f"{key}. {options[key]}")

    print()
# end def

def performWithdrawal(customer_email):
    print("Perform Withdrawal")

    print()

    print("Select the account to withdraw:")

    print()

    accounts = getAccountsByEmail(customer_email)

    printCustomerAccounts(accounts)

    opt = int(input("Enter your choice: "))

    print()

    transaction_amount = float(input("Enter the amount to withdraw: ").strip() or 0)

    if transaction_amount <= 0: # checks whether the amount is greater than 0
        input("The amount to withdraw must be greater than 0. Press \"enter\" to cotinue...")
        return
    # end if

    account_number = accounts[opt - 1]["account_number"]

    print("Select the method to perform the withdrawal:")

    printWithdrawalMethods()

    opt = int(input("Enter your choice: "))

    withdrawal_method = ""

    if opt == 1: withdrawal_method = "ATM"
    elif opt == 2: withdrawal_method = "cashier"

    transaction = {
        "customer_email": customer_email,
        "account_number": account_number,

        "transaction_type": "withdrawal",
        "transaction_amount": transaction_amount,
        "transaction_details": { "withdrawal_method": withdrawal_method } 
    }

    res = performTransactionRequest(transaction)

    if not res.ok: print(f"Failed to perform withdrawal: {res.json()}")
    else: print(f"Withdrawal performed successfully! {transaction}")
# end def

def getAccountByNumber(beneficiary_account_number):
    # request
    suffix = f"/accounts/{beneficiary_account_number}"

    endpoint = f"{API_URL}{suffix}"

    return requests.get(endpoint)
# end def

def performTransfer(customer_email):
    print("Perform Transfer")

    print()

    print("Select the payer account:")

    print()

    accounts = getAccountsByEmail(customer_email)

    printCustomerAccounts(accounts)

    opt = int(input("Enter your choice: "))

    print()

    transaction_amount = float(input("Enter the amount to transfer: ").strip() or 0)

    if transaction_amount <= 0: # checks whether the amount is greater than 0
        input("The amount to transfer must be greater than 0. Press \"enter\" to cotinue...")
        return
    # end if

    account_number = accounts[opt - 1]["account_number"]

    beneficiary_account_number = input("Enter the beneficiary account number: ")

    beneficiaryAccountRes = getAccountByNumber(beneficiary_account_number)

    if not beneficiaryAccountRes.ok:
        print(f"Failed to retrieve beneficiary account: {res.json()}")
        return
    # end if

    print()

    transfer_concept = input("Concept of the transfer: ")

    transaction = {
        "customer_email": customer_email,
        "account_number": account_number,

        "transaction_type": "transfer",
        "transaction_amount": transaction_amount,
        "transaction_details": {
            "payer_account_number": account_number,
            "beneficiary_account_number": beneficiary_account_number,
            "transfer_concept": transfer_concept
        }
    }

    res = performTransactionRequest(transaction)

    if not res.ok: print(f"Failed to perform deposit: {res.json()}")
    else: print(f"Deposit performed successfully! {transaction}")
# end def

def performTransaction(customer_email):
    while (True):
        print("Perform Transaction")

        print()

        printTransactionMenu()

        opt = int(input("Enter your choice: "))

        if opt == 0: return
        elif opt == 1: performDeposit(customer_email)
        elif opt == 2: performWithdrawal(customer_email)
        elif opt == 3: performTransfer(customer_email)
        # end if-elif
    # end def
# end def

# environment variables
API_URL = os.getenv("API_URL", "http://localhost:8000/api")