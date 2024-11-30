# core modules
import os
import pydgraph

# third-party modules
from dotenv import load_dotenv

# custom modules
import dgraphUtils
import mongodbUtils

def printMenu():
    options = {
        0: "Load data",
        1: "Sign up",
        2: "Create new account",
        3: "Retrieve customer information",
        4: "Perform transaction",
        5: "Dgraph Transaction Menu" 
    }

    for key in options.keys(): print(f"{key}. {options[key]}")

    print()

def printTransactionHistoryMenu():
    """Submenu for transaction history options."""
    print("Transaction History Options:")
    print("1. Show Transaction History")
    print("2. Show Risky Transactions")
    print("3. Show Suspicious Accounts Transactions")
    print("4. Frequent Transactions")
    print("5. Geolocation Flagged Transactions")
    print("6. Card Transactions")
    print("7. IP Address Monitoring")
    print("8. Shared Attribute Detection")
    print()

def handleTransactionHistory():
    """Handles the transaction history options."""
    printTransactionHistoryMenu()

    try:
        option = int(input("Enter your choice: "))

        if option == 3:
            # Implement logic to show transaction history
            print("Showing transaction history...")
        elif option == 4:
            # Implement logic to show risky transactions
            print("Showing risky transactions...")
        elif option == 5:
            # Implement logic to show suspicious accounts transactions
            print("Showing suspicious accounts transactions...")
        elif option == 6:
            # Implement logic for frequent transactions
            print("Showing frequent transactions...")
        elif option == 7:
            # Implement logic for geolocation flagged transactions
            print("Showing geolocation flagged transactions...")
        elif option == 8:
            # Implement logic for card transactions
            print("Showing card transactions...")
        elif option == 9:
            # Implement logic for IP address monitoring
            print("Showing IP address monitoring...")
        elif option == 10:
            # Implement logic for shared attribute detection
            print("Showing shared attribute detection...")
        else:
            print("Invalid option. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def main():
    load_dotenv()  # loads environment variables from .env file

    client_stub = pydgraph.DgraphClientStub('localhost:9080')
    client = pydgraph.DgraphClient(client_stub)

    # environment variables
    CUSTOMER_EMAIL = os.getenv("CUSTOMER_EMAIL", "john.doe@example.com")

    while True:
        printMenu()

        try:
            opt = int(input("Enter your choice: "))

            if opt == 0:
                dgraphUtils.load_data(client)
            elif opt == 1:
                mongodbUtils.signUp()
            elif opt == 2:
                mongodbUtils.createAccount(CUSTOMER_EMAIL)
            elif opt == 3:
                mongodbUtils.retrieveCustomerInformation(CUSTOMER_EMAIL)
            elif opt == 4:
                mongodbUtils.performTransaction(CUSTOMER_EMAIL)
            elif opt == 5:
                handleTransactionHistory()  
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
