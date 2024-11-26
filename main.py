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
        2: "Create new account"
    }

    for key in options.keys(): print(f"{key}. {options[key]}")

    print()
# end def

def main():
    load_dotenv() # loads environment variables from .env file

    # environment variables
    USER_EMAIL = os.getenv("USER_EMAIL")

    while (True):
        printMenu()

        opt = int(input("Enter your choice: "))

        if opt == 0: break
        elif opt == 1: mongodbUtils.signUp()
        elif opt == 2: mongodbUtils.createNewAccount(USER_EMAIL)
    # end while
# end def

if __name__ == '__main__':
    try: main()
    except Exception as e: print(f"Error: {e}")
# end if