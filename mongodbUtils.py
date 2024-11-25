# core modules
import os

# third-party modules
from dotenv import load_dotenv
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

    if not res.ok: print(f"Failed to post customer: {res}")
    else: print(f"Customer created successfully! {customer}")
# end def

# environment variables
API_URL = os.getenv("API_URL", "http://localhost:8000/api")