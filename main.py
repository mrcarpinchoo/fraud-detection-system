#!/usr/bin/env python3

# core modules
import os

# third-party modules
from dotenv import load_dotenv

# custom modules
import mongodbUtils

def printMenu():
    options = {
        0: "Exit",
        1: "Sign up",
        2: "Create new account",
        3: "Retrieve customer information",
        4: "Perform transaction"
    }

    for key in options.keys(): print(f"{key}. {options[key]}")

    print()
# end def

def main():
    load_dotenv() # loads environment variables from .env file

    # environment variables
    CUSTOMER_EMAIL = os.getenv("CUSTOMER_EMAIL", "lionel.messi@iteso.mx")

    while (True):
        printMenu()

        opt = int(input("Enter your choice: "))

        if opt == 0: break
        elif opt == 1: mongodbUtils.signUp()
        elif opt == 2: mongodbUtils.createAccount(CUSTOMER_EMAIL)
        elif opt == 3: mongodbUtils.retrieveCustomerInformation(CUSTOMER_EMAIL)
        elif opt == 4: mongodbUtils.performTransaction(CUSTOMER_EMAIL)
    # end while
# end def

if __name__ == '__main__':
    try: main()
    except Exception as e: print(f"Error: {e}")
# end if