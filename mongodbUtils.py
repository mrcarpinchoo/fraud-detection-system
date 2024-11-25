# third-party modules
import requests

def signUp(apiUrl):
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

    endpoint = f"{apiUrl}{suffix}"

    res = requests.post(endpoint, json = customer)

    if not res.ok: print(f"Failed to post customer: {res}")
    else: print(f"Customer created successfully! {customer}")
# end def