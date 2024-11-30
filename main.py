#!/usr/bin/env python3

# core modules
import os, pydgraph

# third-party modules
from dotenv import load_dotenv
import dgraph.client

# custom modules
import dgraphUtils, mongodbUtils, cassandraUtils
import mongodb.data.data as mongodb_data
import json

client_stub = pydgraph.DgraphClientStub('localhost:9080')
dgraph_client = pydgraph.DgraphClient(client_stub)

session = cassandraUtils.connect_to_cassandra()
with open("example_data.json", "r") as file:
    data = json.load(file)

def printMenu():
    options = {
        0: "Load data",
        1: "Sign up",
        2: "Create new account",
        3: "Retrieve customer information",
        4: "Perform transaction",
        5: "Dgraph Transaction Menu",
        6: "Generate transaction summary",
        7: "Cassandra Transaction Menu",
        8: "Exit"
    }

    for key in options.keys(): print(f"{key}. {options[key]}")

    print()

def printTransactionHistoryMenu():
    """Submenu for transaction history options."""
    print("Transaction History Options:")
    print("1. Show Customer Information")
    print("2. Show Transaction History")
    print("3. Show Risky Transactions")
    print("4. Show Suspicious Accounts Transactions")
    print("5. Frequent Transactions")
    print("6. Geolocation Flagged Transactions")
    print("7. Card Transactions")
    print("8. IP Address Monitoring")
    print("9. Shared Attribute Detection")
    print()

def handleTransactionHistory():
    """Handles the transaction history options."""
    printTransactionHistoryMenu()

    try:
        option = int(input("Enter your choice: "))

        if option == 1:
            dgraph.client.query_customer_info()
        elif option == 2:
            dgraph.client.query_transaction_history()
        elif option == 3:
            dgraph.client.query_risky_transactions()
        elif option == 4:
            dgraph.client.query_suspicious_accounts()
        elif option == 5:
            dgraph.client.query_frequent_transactions()
        elif option == 6:
            dgraph.client.query_transactions_in_risky_locations() 
        elif option == 7:
            dgraph.client.query_cards_by_type("Visa") 
        elif option == 8:
            dgraph.client.query_ip_addresses_and_customers()
        elif option == 9:
            dgraph.client.query_customers_with_duplicate_attributes()
        else:
            print("Invalid option. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def printTransactionHistoryCassandraMenu():
    """Submenu for transaction history options."""
    print("Transaction History Options:")
    print("1. Show Recent Transaction")
    print("2. Show Withdrawal Transactions")
    print("3. Show Transactions with Anomalies")
    print("4. Show Customer Login History")
    print("5. Show Cross Border Transactions")
    print()

def handleTransactionHistoryCassandra():
    """Handles the transaction history options."""
    printTransactionHistoryCassandraMenu()

    try:
        option = int(input("Enter your choice: "))

        if option == 1:
            cassandraUtils.query_recent_transactions(session, limit=10)
        elif option == 2:
            cassandraUtils.query_withdrawals(session)
        elif option == 3:
            cassandraUtils.query_anomalies(session)
        elif option == 4:
            cassandraUtils.query_login_attempts(session, limit=5)
        elif option == 5:
            cassandraUtils.query_cross_border_transactions(session)
        else:
            print("Invalid option. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")


def main():
    load_dotenv()  # loads environment variables from .env file
    

    # environment variables
    CUSTOMER_EMAIL = os.getenv("CUSTOMER_EMAIL", "john.doe@example.com")

    while True:
        printMenu()

        try:
            opt = int(input("Enter your choice: "))

            if opt == 0:
                '''mongodb_data.load_data_from_json()
                dgraphUtils.load_data(dgraph_client)'''
                cassandraUtils.bulk_insert_from_json(session, data)
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
            elif opt == 6:
                mongodbUtils.generateTransactionSummary(CUSTOMER_EMAIL)
            elif opt == 7:
                handleTransactionHistoryCassandra()
            elif opt == 8: break
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
