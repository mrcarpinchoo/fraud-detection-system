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
        1: "Sign up"
    }

    for key in options.keys(): print(f"{key}. {options[key]}")

    print()
# end def

# environment variables
API_URL = os.getenv("API_URL", "http://localhost:8000/api")

USER_EMAIL = os.getenv("USER_EMAIL")

load_dotenv() # loads environment variables from .env file

def main():
    while (True):
        printMenu()

        opt = int(input("Enter your choice: "))

        if opt == 0: break
        elif opt == 1: mongodbUtils.signUp(API_URL)
    # end while
# end def

if __name__ == '__main__':
    try: main()
    except Exception as e: print(f"Error: {e}")
# end if