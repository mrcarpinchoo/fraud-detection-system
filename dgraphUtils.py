import pydgraph
import json
from datetime import datetime, timedelta
import random

def create_schema(client):
    """Creates the schema in Dgraph before inserting data."""
    schema = """
    type Customer {
        customer_id: string
        name: string
        address: string
        email: string
        risk_score: float
        transactions: [Transaction]
        accounts: [Account]
        sessions: [Session]
    }

    type Transaction {
        transaction_id: string
        amount: float
        status: string
        date: datetime
        is_risky: bool
        linked_customer: Customer
        linked_geolocation: Geolocation
        session: Session
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
        card: Card
        ip_address: IPAddress
        attributes: [Attribute]
    }

    type Device {
        device_id: string
        device_type: string
        linked_account: Account
    }

    type Session {
        session_id: string
        start_time: datetime
        end_time: datetime
        ip_address: IPAddress
    }

    type Card {
        card_id: string
        card_type: string
        expiration_date: datetime
    }

    type IPAddress {
        ip: string
        ip_location: string
    }

    type Attribute {
        attribute_name: string
        attribute_value: string
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
    session: uid . 
    linked_geolocation: uid . 

    location: string @index(exact) . 
    latitude: float . 
    longitude: float . 

    account_id: string @index(exact) . 
    account_type: string @index(exact) . 
    balance: float . 

    device_id: string @index(exact) . 
    device_type: string @index(exact) . 

    session_id: string @index(exact) . 
    start_time: datetime . 
    end_time: datetime . 

    card_id: string @index(exact) . 
    card_type: string @index(exact) . 
    expiration_date: datetime . 

    ip: string @index(exact) . 
    ip_location: string . 

    attribute_name: string @index(exact) . 
    attribute_value: string . 

    transactions: [uid] @reverse . 
    linked_customer: uid @reverse .  
    accounts: [uid] @reverse . 
    devices: [uid] @reverse . 
    linked_account: uid @reverse . 
    sessions: [uid] @reverse . 
    card: uid . 
    ip_address: uid . 
    attributes: [uid] @reverse . 
    """
    op = pydgraph.Operation(schema=schema)
    client.alter(op)
    print("Schema created successfully.")

sample_data = {
    "customers": [
        {
            "customer_id": f"CUST{i:03d}",
            "name": f"Customer {i}",
            "address": f"{random.randint(100, 999)} Main Street",
            "email": f"customer{i}@example.com",
            "risk_score": round(random.uniform(0.1, 0.9), 2)
        } for i in range(1, 21) 
    ],
    
    "geolocations": [
        {
            "location": city,
            "latitude": coords[0],
            "longitude": coords[1]
        } for city, coords in {
            "New York": (40.7128, -74.0060),
            "Los Angeles": (34.0522, -118.2437),
            "Chicago": (41.8781, -87.6298),
            "Houston": (29.7604, -95.3698),
            "Phoenix": (33.4484, -112.0740)
        }.items()
    ],
    
    "accounts": [
        {
            "account_id": f"ACC{i:03d}",
            "account_type": random.choice(["Savings", "Checking", "Investment"]),
            "balance": round(random.uniform(1000, 100000), 2)
        } for i in range(1, 41)  
    ],
    
    "devices": [
        {
            "device_id": f"DEV{i:03d}",
            "device_type": random.choice(["Smartphone", "Tablet", "Desktop", "Laptop"])
        } for i in range(1, 61)  
    ],
    
    "transactions": [
        {
            "transaction_id": f"TXN{i:03d}",
            "amount": round(random.uniform(10, 5000), 2),
            "status": random.choice(["completed", "pending", "failed"]),
            "date": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "is_risky": random.choice([True, False]),
            "receiving_account": f"ACC{random.randint(1, 40):03d}"
        } for i in range(1, 101) 
    ],
    
    "sessions": [
        {
            "session_id": f"SESSION{i:03d}",
            "start_time": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "ip_address": f"192.168.1.{random.randint(1, 255)}"
        } for i in range(1, 21)  
    ],
    
    "cards": [
        {
            "card_id": f"CARD{i:03d}",
            "card_type": random.choice(["Visa", "MasterCard", "American Express"]),
            "expiration_date": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%dT%H:%M:%SZ")
        } for i in range(1, 21)  
    ],
    
    "ip_addresses": [
        {
            "ip": f"192.168.1.{random.randint(1, 255)}",
            "ip_location": random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"])
        } for _ in range(1, 21)  
    ],
    
    "attributes": [
        {
            "attribute_name": f"Attribute {i}",
            "attribute_value": f"Value {random.randint(1, 100)}"
        } for i in range(1, 21)  
    ]
}

def bulk_insert_data(client):
    """
    Bulk inserts the sample data into Dgraph database.
    """
    uids = {
        "customers": {},
        "geolocations": {},
        "accounts": {},
        "devices": {},
        "cards": {},
        "ip_addresses": {},
        "attributes": {}
    }

    for customer in sample_data["customers"]:
        txn = client.txn()
        try:
            customer_data = {
                "uid": "_:customer",
                **customer
            }
            resp = txn.mutate(set_obj=customer_data)
            txn.commit()
            uids["customers"][customer["customer_id"]] = resp.uids["customer"]
        except Exception as e:
            print(f"Error creating customer {customer['customer_id']}: {e}")
        finally:
            txn.discard()

    for geolocation in sample_data["geolocations"]:
        txn = client.txn()
        try:
            geolocation_data = {
                "uid": "_:geolocation",
                **geolocation
            }
            resp = txn.mutate(set_obj=geolocation_data)
            txn.commit()
            uids["geolocations"][geolocation["location"]] = resp.uids["geolocation"]
        except Exception as e:
            print(f"Error creating geolocation {geolocation['location']}: {e}")
        finally:
            txn.discard()

    for idx, account in enumerate(sample_data["accounts"]):
        txn = client.txn()
        try:
            customer_id = f"CUST{(idx // 2 + 1):03d}"
            account_data = {
                "uid": "_:account",
                **account,
                "linked_customer": {"uid": uids["customers"][customer_id]}
            }
            resp = txn.mutate(set_obj=account_data)
            txn.commit()
            uids["accounts"][account["account_id"]] = resp.uids["account"]

            link_account_to_customer(
                client,
                uids["customers"][customer_id],
                resp.uids["account"]
            )
        except Exception as e:
            print(f"Error creating account {account['account_id']}: {e}")
        finally:
            txn.discard()

    for idx, device in enumerate(sample_data["devices"]):
        txn = client.txn()
        try:
            account_id = f"ACC{(idx // 2 + 1):03d}"
            device_data = {
                "uid": "_:device",
                **device,
                "linked_account": {"uid": uids["accounts"][account_id]}
            }
            resp = txn.mutate(set_obj=device_data)
            txn.commit()
            uids["devices"][device["device_id"]] = resp.uids["device"]
            
            link_device_to_account(
                client,
                uids["accounts"][account_id],
                resp.uids["device"]
            )
        except Exception as e:
            print(f"Error creating device {device['device_id']}: {e}")
        finally:
            txn.discard()

    for card in sample_data["cards"]:
        txn = client.txn()
        try:
            card_data = {
                "uid": "_:card",
                **card
            }
            resp = txn.mutate(set_obj=card_data)
            txn.commit()
            uids["cards"][card["card_id"]] = resp.uids["card"]

            account_id = f"ACC{random.randint(1, 40):03d}"
            link_card_to_account(client, uids["accounts"][account_id], resp.uids["card"])
        except Exception as e:
            print(f"Error creating card {card['card_id']}: {e}")
        finally:
            txn.discard()

    for ip_address in sample_data["ip_addresses"]:
        txn = client.txn()
        try:
            ip_address_data = {
                "uid": "_:ip_address",
                **ip_address
            }
            resp = txn.mutate(set_obj=ip_address_data)
            txn.commit()
            uids["ip_addresses"][ip_address["ip"]] = resp.uids["ip_address"]

            account_id = f"ACC{random.randint(1, 40):03d}"
            link_ip_address_to_account(client, uids["accounts"][account_id], resp.uids["ip_address"])
        except Exception as e:
            print(f"Error creating IP address {ip_address['ip']}: {e}")
        finally:
            txn.discard()

    for attribute in sample_data["attributes"]:
        txn = client.txn()
        try:
            attribute_data = {
                "uid": "_:attribute",
                **attribute
            }
            resp = txn.mutate(set_obj=attribute_data)
            txn.commit()
            uids["attributes"][attribute["attribute_name"]] = resp.uids["attribute"]

            account_id = f"ACC{random.randint(1, 40):03d}"
            link_attribute_to_account(client, uids["accounts"][account_id], resp.uids["attribute"])
        except Exception as e:
            print(f"Error creating attribute {attribute['attribute_name']}: {e}")
        finally:
            txn.discard()

    for transaction in sample_data["transactions"]:
        txn = client.txn()
        try:
            random_customer_id = f"CUST{random.randint(1, 20):03d}"
            random_geolocation = random.choice(sample_data["geolocations"])["location"]
            
            transaction_data = {
                "uid": "_:transaction",
                **transaction,
                "linked_customer": {"uid": uids["customers"][random_customer_id]},
                "linked_geolocation": {"uid": uids["geolocations"][random_geolocation]}
            }
            resp = txn.mutate(set_obj=transaction_data)
            txn.commit()
        except Exception as e:
            print(f"Error creating transaction {transaction['transaction_id']}: {e}")
        finally:
            txn.discard()

def link_card_to_account(client, account_uid, card_uid):
    """Helper function to link card to account"""
    txn = client.txn()
    try:
        mutation = {
            "uid": account_uid,
            "card": {"uid": card_uid}
        }
        txn.mutate(set_obj=mutation)
        txn.commit()
    except Exception as e:
        print(f"Error linking card to account: {e}")
    finally:
        txn.discard()

def link_ip_address_to_account(client, account_uid, ip_address_uid):
    """Helper function to link IP address to account"""
    txn = client.txn()
    try:
        mutation = {
            "uid": account_uid,
            "ip_address": {"uid": ip_address_uid}
        }
        txn.mutate(set_obj=mutation)
        txn.commit()
    except Exception as e:
        print(f"Error linking IP address to account: {e}")
    finally:
        txn.discard()

def link_attribute_to_account(client, account_uid, attribute_uid):
    """Helper function to link attribute to account"""
    txn = client.txn()
    try:
        mutation = {
            "uid": account_uid,
            "attributes": [{"uid": attribute_uid}]
        }
        txn.mutate(set_obj=mutation)
        txn.commit()
    except Exception as e:
        print(f"Error linking attribute to account: {e}")
    finally:
        txn.discard()


def link_account_to_customer(client, customer_uid, account_uid):
    """Helper function to link account to customer"""
    txn = client.txn()
    try:
        mutation = {
            "uid": customer_uid,
            "accounts": [{"uid": account_uid}]
        }
        txn.mutate(set_obj=mutation)
        txn.commit()
    except Exception as e:
        print(f"Error linking account to customer: {e}")
    finally:
        txn.discard()

def link_device_to_account(client, account_uid, device_uid):
    """Helper function to link device to account"""
    txn = client.txn()
    try:
        mutation = {
            "uid": account_uid,
            "devices": [{"uid": device_uid}]
        }
        txn.mutate(set_obj=mutation)
        txn.commit()
    except Exception as e:
        print(f"Error linking device to account: {e}")
    finally:
        txn.discard()

def drop_all_data(client):
    """Drops all data in the Dgraph database before performing the bulk insert."""
    try:
        op = pydgraph.Operation(drop_all=True)
        client.alter(op)
        print("All data dropped successfully.")
    except Exception as e:
        print(f"Error dropping data: {e}")

def load_data(client):
    """Drops data, creates the schema, and performs bulk data insertion."""
    drop_all_data(client) 
    create_schema(client)   
    bulk_insert_data(client)  

