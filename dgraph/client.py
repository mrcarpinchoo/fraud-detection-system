import pydgraph
import json
import os

client_stub = pydgraph.DgraphClientStub('localhost:9080')
client = pydgraph.DgraphClient(client_stub)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_schema():
    schema = """
    type Customer {
        customer_id: string
        name: string
        address: string
        email: string
        risk_score: float
        transactions: [Transaction]
        accounts: [Account]
    }

    type Transaction {
        transaction_id: string
        amount: float
        status: string
        date: datetime
        is_risky: bool
        linked_customer: Customer
        linked_geolocation: Geolocation
        receiving_account: string
    }

    type Geolocation {
        location: string
        latitude: float
        longitude: float
    }

    type Account {
        account_id: string
        account_type: string
        balance: float
        linked_customer: Customer
        devices: [Device]
    }

    type Device {
        device_id: string
        device_type: string
        linked_account: Account
    }

    customer_id: string @index(exact) . 
    name: string . 
    address: string . 
    email: string . 
    risk_score: float . 

    transaction_id: string @index(exact) . 
    amount: float @index(float) . 
    status: string @index(exact) . 
    date: datetime . 
    is_risky: bool @index(bool) .   
    receiving_account: string @index(exact) .  

    location: string @index(exact) . 
    latitude: float . 
    longitude: float . 

    account_id: string @index(exact) . 
    account_type: string @index(exact) . 
    balance: float . 

    device_id: string @index(exact) . 
    device_type: string @index(exact) . 

    transactions: [uid] @reverse . 
    linked_customer: uid @reverse . 
    linked_geolocation: uid . 
    accounts: [uid] @reverse . 
    devices: [uid] @reverse . 
    linked_account: uid @reverse . 
    """
    op = pydgraph.Operation(schema=schema)
    client.alter(op)
    print("Schema created successfully.")

def create_customer():
    txn = client.txn()
    try:
        customer_data = {
            "uid": "_:customer",
            "customer_id": "CUST123",
            "name": "John Doe",
            "address": "123 Elm Street",
            "email": "johndoe@example.com",
            "risk_score": 0.5
        }
        resp = txn.mutate(set_obj=customer_data)
        txn.commit()
        print(f"Customer created: {customer_data}")
        return resp.uids["customer"]
    except Exception as e:
        print(f"Error creating customer: {e}")
    finally:
        txn.discard()

def create_geolocation():
    txn = client.txn()
    try:
        geolocation_data = {
            "uid": "_:geolocation",
            "location": "Los Angeles",
            "latitude": 34.0522,
            "longitude": -118.2437
        }
        resp = txn.mutate(set_obj=geolocation_data)
        txn.commit()
        print(f"Geolocation created: {geolocation_data}")
        return resp.uids["geolocation"]
    except Exception as e:
        print(f"Error creating geolocation: {e}")
    finally:
        txn.discard()

def create_transaction(customer_uid, geolocation_uid):
    clear_screen()
    print("---- Make Transaction ----")
    receiving_account = input("Enter Receiving Account ID: ")
    amount = float(input("Enter Transaction Amount: "))

    txn = client.txn()
    try:
        transaction_data = {
            "uid": "_:transaction",
            "transaction_id": "TXN001",
            "amount": amount,
            "status": "pending",
            "date": "2024-11-24T10:00:00Z",
            "is_risky": True,
            "linked_customer": {"uid": customer_uid},
            "linked_geolocation": {"uid": geolocation_uid},
            "receiving_account": receiving_account
        }

        customer_city = "New York"
        geolocation_city = "Los Angeles"

        if customer_city == geolocation_city:
            transaction_data["is_risky"] = False

        resp = txn.mutate(set_obj=transaction_data)
        txn.commit()

        if transaction_data["is_risky"]:
            print("Warning: This transaction is flagged as risky.")

        print(f"Transaction created successfully")
    finally:
        txn.discard()

    input("Press Enter to go back to the main menu...")

def create_account(customer_uid):
    txn = client.txn()
    try:
        account_data = {
            "uid": "_:account",
            "account_id": "ACC123",
            "account_type": "Savings",
            "balance": 1000.00,
            "linked_customer": {"uid": customer_uid}
        }
        resp = txn.mutate(set_obj=account_data)
        txn.commit()
        print(f"Account created: {account_data}")
        return resp.uids["account"]
    except Exception as e:
        print(f"Error creating account: {e}")
    finally:
        txn.discard()

def create_device(account_uid):
    txn = client.txn()
    try:
        device_data = {
            "uid": "_:device",
            "device_id": "DEV123",
            "device_type": "Smartphone",
            "linked_account": {"uid": account_uid}
        }
        resp = txn.mutate(set_obj=device_data)
        txn.commit()
        print(f"Device created: {device_data}")
        return resp.uids["device"]
    except Exception as e:
        print(f"Error creating device: {e}")
    finally:
        txn.discard()

def link_account_to_customer(customer_uid, account_uid):
    txn = client.txn()
    try:
        mutation = {
            "uid": customer_uid,
            "accounts": [{"uid": account_uid}]
        }
        txn.mutate(set_obj=mutation)
        txn.commit()
        print(f"Account linked to customer: {customer_uid}")
    except Exception as e:
        print(f"Error linking account to customer: {e}")
    finally:
        txn.discard()

def link_device_to_account(account_uid, device_uid):
    txn = client.txn()
    try:
        mutation = {
            "uid": account_uid,
            "devices": [{"uid": device_uid}]
        }
        txn.mutate(set_obj=mutation)
        txn.commit()
        print(f"Device linked to account: {account_uid}")
    except Exception as e:
        print(f"Error linking device to account: {e}")
    finally:
        txn.discard()

def query_transaction_history():
    clear_screen()
    query = """
    {
        transactions(func: has(transaction_id)) {
            uid
            transaction_id
            amount
            status
            date
            is_risky
            receiving_account
            linked_customer {
                customer_id
                name
            }
            linked_geolocation {
                location
                latitude
                longitude
            }
        }
    }
    """

    res = client.txn(read_only=True).query(query)
    parsed_res = json.loads(res.json.decode('utf-8'))

    print("Transaction History:")
    print(json.dumps(parsed_res, indent=4))

    input("Press Enter to go back to the main menu...")

def query_accounts_and_devices(customer_uid):
    clear_screen()
    query = f"""
    {{
        customer(func: uid({customer_uid})) {{
            name
            accounts {{
                account_id
                account_type
                balance
                devices {{
                    device_id
                    device_type
                }}
            }}
        }}
    }}
    """
    res = client.txn(read_only=True).query(query)
    parsed_res = json.loads(res.json.decode('utf-8'))
    print("Customer Accounts and Devices:")
    print(json.dumps(parsed_res, indent=4))

    input("Press Enter to go back to the main menu...")

def query_risky_transactions():
    clear_screen()
    query = """
    {
        risky_transactions(func: has(is_risky)) @filter(eq(is_risky, true)) {
            transaction_id
            amount
            status
            date
            receiving_account
        }
    }
    """
    res = client.txn(read_only=True).query(query)
    parsed_res = json.loads(res.json.decode('utf-8'))
    print("Risky Transactions:")
    print(json.dumps(parsed_res, indent=4))

    input("Press Enter to go back to the main menu...")

def query_suspicious_accounts():
    clear_screen()
    suspicious_accounts = ["A001", "A003", "A004"]

    suspicious_accounts_str = '", "'.join(suspicious_accounts)
    
    query = f"""
    {{
        suspicious_transactions(func: has(receiving_account)) @filter(eq(receiving_account, "{suspicious_accounts_str}")) {{
            transaction_id
            amount
            status
            date
            receiving_account
        }}
    }}
    """
    res = client.txn(read_only=True).query(query)
    parsed_res = json.loads(res.json.decode('utf-8'))
    print("Suspicious Accounts Transactions:")
    print(json.dumps(parsed_res, indent=4))

    input("Press Enter to go back to the main menu...")

def main_menu(customer_uid, geolocation_uid):
    while True:
        clear_screen()
        print("\n---- Transaction Menu ----")
        print("1. View Accounts and Devices")
        print("2. Make Transaction")
        print("3. Show Transaction History")
        print("4. Show Risky Transactions")
        print("5. Show Suspicious Accounts Transactions")
        print("6. Frequent Transactions")
        print("7. Geolocation Flagged Transactions")
        print("8. Card Transactions")
        print("9. IP Address Monitoring")
        print("10. Shared Attribute Detection")
        print("11. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            query_accounts_and_devices(customer_uid)
        elif choice == "2":
            create_transaction(customer_uid, geolocation_uid)
        elif choice == "3":
            query_transaction_history()  
        elif choice == "4":
            query_risky_transactions()
        elif choice == "5":
            query_suspicious_accounts()
        elif choice == "6":
            print("Frequent Transactions feature is not implemented yet.")
            input("Press Enter to continue...")
        elif choice == "7":
            print("Geolocation Flagged Transactions feature is not implemented yet.")
            input("Press Enter to continue...")
        elif choice == "8":
            print("Card Transactions feature is not implemented yet.")
            input("Press Enter to continue...")
        elif choice == "9":
            print("IP Address Monitoring feature is not implemented yet.")
            input("Press Enter to continue...")
        elif choice == "10":
            print("Shared Attribute Detection feature is not implemented yet.")
            input("Press Enter to continue...")
        elif choice == "11":
            break
        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    create_schema()
    customer_uid = create_customer()
    geolocation_uid = create_geolocation()
    account_uid = create_account(customer_uid)
    device_uid = create_device(account_uid)

    link_account_to_customer(customer_uid, account_uid)
    link_device_to_account(account_uid, device_uid)
    
    main_menu(customer_uid, geolocation_uid)
