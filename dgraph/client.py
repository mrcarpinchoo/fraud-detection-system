import pydgraph
import json
import os

client_stub = pydgraph.DgraphClientStub('localhost:9080')
client = pydgraph.DgraphClient(client_stub)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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
    suspicious_accounts = ["ACC030", "ACC038", "ACC049", "ACC020", "ACC021", "ACC019"]       # hardcoded suspicious accounts

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

def query_customer_info():
    clear_screen()
    query = """
    {
      customers(func: has(customer_id)) {
        uid
        customer_id
        name
        address
        email
        risk_score
        accounts {
          account_id
          account_type
          balance
          devices {
            device_id
            device_type
          }
          attributes {
            attribute_name
            attribute_value
          }
          ip_address {
            ip
            ip_location
          }
        }
      }
    }
    """
    
    res = client.txn(read_only=True).query(query)
    parsed_res = json.loads(res.json.decode('utf-8'))

    print("Customer Information:")
    print(json.dumps(parsed_res, indent=4))

    input("Press Enter to go back to the main menu...")

def query_frequent_transactions():
    clear_screen()

    query = """
    {
      transactions(func: has(receiving_account)) {
        transaction_id
        amount
        status
        date
        receiving_account
        linked_customer {
          customer_id
          name
        }
      }
    }
    """

    try:
        res = client.txn(read_only=True).query(query)
        parsed_res = json.loads(res.json.decode('utf-8'))

        account_transaction_count = {}

        for transaction in parsed_res.get("transactions", []):
            receiving_account = transaction.get("receiving_account")
            if receiving_account:
                account_transaction_count[receiving_account] = account_transaction_count.get(receiving_account, 0) + 1

        filtered_transactions = []
        for account, count in account_transaction_count.items():
            if count > 20:
                account_transactions = [txn for txn in parsed_res["transactions"] if txn["receiving_account"] == account]
                filtered_transactions.append({
                    "receiving_account": account,
                    "total_transactions": count,
                    "transactions": account_transactions
                })

        if filtered_transactions:
            print("Transactions for receiving accounts with more than 20 transactions:")
            print(json.dumps(filtered_transactions, indent=4))
        else:
            print("No accounts have more than 20 transactions.")

    except Exception as e:
        print(f"Error querying frequent transactions: {e}")

    input("Press Enter to go back to the main menu...")

def query_transactions_in_risky_locations():
    """
    Queries transactions linked to geolocations in Chicago.
    """
    clear_screen()
    
    query = """
    {
        chicago_geolocation(func: eq(location, "Chicago")) {
            location
            latitude
            longitude
            ~linked_geolocation {
                transaction_id
                amount
                status
                date
                receiving_account
                linked_customer {
                    customer_id
                    name
                }
            }
        }
    }
    """
    
    try:
        res = client.txn(read_only=True).query(query)
        parsed_res = json.loads(res.json.decode('utf-8'))
        
        print("Transactions Linked to Chicago:")
        print(json.dumps(parsed_res, indent=4))
    except Exception as e:
        print(f"Error querying transactions in Chicago: {e}")

    input("Press Enter to go back to the main menu...")

def query_ip_addresses_and_customers():
    """
    Queries IP addresses and their linked accounts and customers in reverse.
    """
    clear_screen()
    
    query = """
    {
        ip_addresses(func: has(ip)) {
            ip
            ip_location
            ~ip_address {
                account_id
                account_type
                balance
                linked_customer {
                    customer_id
                    name
                }
            }
        }
    }
    """
    
    try:
        res = client.txn(read_only=True).query(query)
        parsed_res = json.loads(res.json.decode('utf-8'))
        
        print("IP Addresses and Linked Accounts/Customers:")
        print(json.dumps(parsed_res, indent=4))
    except Exception as e:
        print(f"Error querying IP addresses and their linked accounts/customers: {e}")

    input("Press Enter to go back to the main menu...")

def query_cards_by_type(card_type):
    """
    Queries for cards of a specific type and retrieves linked account and transaction details.
    """
    clear_screen()

    query = f"""
    {{
        cards(func: has(card_type)) @filter(eq(card_type, "{card_type}")) {{
            card_id
            card_type
            ~card {{
                account_id
                account_type
                balance
                linked_customer {{
                    customer_id
                    name
                    ~linked_customer {{
                        transaction_id
                        amount
                        status
                        date
                        receiving_account
                    }}
                }}
            }}
        }}
    }}
    """
    
    try:
        res = client.txn(read_only=True).query(query)
        parsed_res = json.loads(res.json.decode('utf-8'))
        
        print(f"Cards of type {card_type}:")
        print(json.dumps(parsed_res, indent=4))
    except Exception as e:
        print(f"Error querying cards by type: {e}")

    input("Press Enter to go back to the main menu...")

def query_customers_with_duplicate_attributes():
    clear_screen()

    query = """
    {
      customers_with_duplicate_attributes(func: has(customer_id)) {
        customer_id
        name
        address
        email
        transactions {
          transaction_id
          amount
          status
          date
          receiving_account
        }
      }
    }
    """

    try:
        res = client.txn(read_only=True).query(query)
        parsed_res = json.loads(res.json.decode('utf-8'))

        grouped_by_address = {}
        grouped_by_email = {}
        grouped_by_name = {}

        for customer in parsed_res.get("customers_with_duplicate_attributes", []):
            if customer.get("address"):
                if customer["address"] not in grouped_by_address:
                    grouped_by_address[customer["address"]] = []
                grouped_by_address[customer["address"]].append(customer)

            if customer.get("email"):
                if customer["email"] not in grouped_by_email:
                    grouped_by_email[customer["email"]] = []
                grouped_by_email[customer["email"]].append(customer)

            if customer.get("name"):
                if customer["name"] not in grouped_by_name:
                    grouped_by_name[customer["name"]] = []
                grouped_by_name[customer["name"]].append(customer)

        duplicates_found = False
        for group in [grouped_by_address, grouped_by_email, grouped_by_name]:
            for key, group_customers in group.items():
                if len(group_customers) > 1:
                    duplicates_found = True
                    print(f"Customers with the same {list(group.keys())[0]}: {key}")
                    print(json.dumps(group_customers, indent=4))

        if not duplicates_found:
            print("No customers found with the same address, email, or name.")

    except Exception as e:
        print(f"Error querying customers with duplicate attributes: {e}")

    input("Press Enter to go back to the main menu...")
