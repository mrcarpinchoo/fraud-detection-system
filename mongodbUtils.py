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

def createNewAccount(customerEmail):
    print("Create New Account")

    customer = getCustomerByEmail(customerEmail)

    # request
    suffix = f"/customers/{customer['_id']}/accounts"

    endpoint = f"{API_URL}{suffix}"

    res = requests.put(endpoint, json = {})

    if not res.ok: print(f"Failed to post account: {res.json()}")
    else: print(f"Account created successfully! {res.json()}")
# end def

# environment variables
API_URL = os.getenv("API_URL", "http://localhost:8000/api")