from cassandra.cluster import Cluster
import uuid
from datetime import datetime
from config import CASSANDRA_HOSTS, CASSANDRA_PORT, KEYSPACE
import json

with open("example_data.json", "r") as file:
    data = json.load(file)


# =======================
# Cassandra Connection
# =======================

def connect_to_cassandra():
    cluster = Cluster(contact_points=CASSANDRA_HOSTS, port=CASSANDRA_PORT)
    session = cluster.connect()
    return session

# =======================
# Create Keyspace
# =======================

def create_keyspace(session):
    create_keyspace_cql = f"""
    CREATE KEYSPACE IF NOT EXISTS {KEYSPACE}
    WITH replication = {{
        'class': 'SimpleStrategy',
        'replication_factor': '3'
    }};
    """
    session.execute(create_keyspace_cql)

# =======================
# Create Tables
# =======================

def create_tables(session):
    session.set_keyspace(KEYSPACE)

    tables = [
        """
        CREATE TABLE IF NOT EXISTS Transaction_History (
            account_id uuid,
            transaction_timestamp timestamp,
            transaction_id uuid,
            amount decimal,
            transaction_type text,
            location text,
            PRIMARY KEY (account_id, transaction_timestamp)
        ) WITH CLUSTERING ORDER BY (transaction_timestamp DESC);
        """,
        """
        CREATE TABLE IF NOT EXISTS Anomaly_Detection (
            account_id uuid,
            transaction_timestamp timestamp,
            transaction_id uuid,
            anomaly_type text,
            anomaly_score int,
            PRIMARY KEY (account_id, transaction_timestamp)
        ) WITH CLUSTERING ORDER BY (transaction_timestamp DESC);
        """,
        """
        CREATE TABLE IF NOT EXISTS Frequent_Withdrawals (
            account_id uuid,
            transaction_timestamp timestamp,
            transaction_id uuid,
            amount decimal,
            PRIMARY KEY (account_id, transaction_timestamp)
        ) WITH CLUSTERING ORDER BY (transaction_timestamp DESC);
        """,
        """
        CREATE TABLE IF NOT EXISTS Customer_Login_History (
            customer_id uuid,
            login_timestamp timestamp,
            ip_address text,
            login_success boolean,
            PRIMARY KEY (customer_id, login_timestamp)
        ) WITH CLUSTERING ORDER BY (login_timestamp DESC);
        """,
        """
        CREATE TABLE IF NOT EXISTS Cross_Border_Transactions (
            account_id uuid,
            transaction_timestamp timestamp,
            transaction_id uuid,
            foreign_location text,
            amount decimal,
            PRIMARY KEY (account_id, transaction_timestamp)
        ) WITH CLUSTERING ORDER BY (transaction_timestamp DESC);
        """
    ]

    for table_cql in tables:
        session.execute(table_cql)

# =======================
# Insert Data Functions
# =======================

def insert_Customer_Login_History(session, customer, login):
    session.execute("""
        INSERT INTO Customer_Login_History (customer_id, login_timestamp, ip_address, login_success)
        VALUES (%s, %s, %s, %s);
    """, (
        uuid.UUID(customer["customer_id"]),
        datetime.fromtimestamp(login["login_timestamp"]),
        login["ip_address"],
        login["login_success"]
    ))


def insert_Cross_Border_Transactions(session, account, transaction):
    if account["account_original_location"] == transaction["location"]:
        return
    session.execute("""
        INSERT INTO Cross_Border_Transactions (account_id, transaction_timestamp, transaction_id, foreign_location, amount)
        VALUES (%s, %s, %s, %s, %s);
    """, (
        uuid.UUID(account["account_id"]),
        datetime.fromtimestamp(transaction["transaction_timestamp"]),
        uuid.UUID(transaction["transaction_id"]),
        transaction["location"],
        transaction["transaction_amount"]
    ))


def insert_Transaction_History(session, account, transaction):
    session.execute("""
        INSERT INTO Transaction_History (account_id, transaction_timestamp, transaction_id, amount, transaction_type, location)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (
        uuid.UUID(account["account_id"]),
        datetime.fromtimestamp(transaction["transaction_timestamp"]),
        uuid.UUID(transaction["transaction_id"]),
        transaction["transaction_amount"],
        transaction["transaction_type"],
        transaction["location"]
    ))


def insert_Anomaly_Detection(session, account, transaction):
    if transaction["anomaly_score"] < 0.5:
        return
    session.execute("""
        INSERT INTO Anomaly_Detection (account_id, transaction_timestamp, transaction_id, anomaly_type, anomaly_score)
        VALUES (%s, %s, %s, %s, %s);
    """, (
        uuid.UUID(account["account_id"]),
        datetime.fromtimestamp(transaction["transaction_timestamp"]),
        uuid.UUID(transaction["transaction_id"]),
        transaction["anomaly_type"],
        transaction["anomaly_score"]
    ))


def insert_Frequent_Withdrawals(session, account, transaction):
    if transaction["transaction_type"] != "withdrawal":
        return
    session.execute("""
        INSERT INTO Frequent_Withdrawals (account_id, transaction_timestamp, transaction_id, amount)
        VALUES (%s, %s, %s, %s);
    """, (
        uuid.UUID(account["account_id"]),
        datetime.fromtimestamp(transaction["transaction_timestamp"]),
        uuid.UUID(transaction["transaction_id"]),
        transaction["transaction_amount"]
    ))


def bulk_insert_from_json(session, data):
    # Insert customers and login history
    for customer in data.get("customers", []):
        for login in customer.get("logins", []):
            insert_Customer_Login_History(session, customer, login)

    # Insert accounts and related transactions
    for account in data.get("accounts", []):
        for transaction in data.get("transactions", []):
            # Ensure transaction belongs to the current account
            if transaction["account_number"] == account["account_number"]:
                insert_Transaction_History(session, account, transaction)
                insert_Cross_Border_Transactions(session, account, transaction)
                insert_Anomaly_Detection(session, account, transaction)
                insert_Frequent_Withdrawals(session, account, transaction)

# =======================
# Query Functions
# =======================

def query_recent_transactions(session, limit=10):
    query = """
    SELECT * FROM Transaction_History
    LIMIT %s;
    """
    rows = session.execute(query, (limit))
    return list(rows)


def query_anomalies(session):
    query = """
    SELECT * FROM Anomaly_Detection;
    """
    rows = session.execute(query)
    return list(rows)


def query_withdrawals(session):
    query = """
    SELECT * FROM Frequent_Withdrawals;
    """
    rows = session.execute(query)
    return list(rows)


def query_login_attempts(session, limit=5):
    query = """
    SELECT * FROM Customer_Login_History
    LIMIT %s;
    """
    rows = session.execute(query, (limit))
    return list(rows)


def query_cross_border_transactions(session):
    query = """
    SELECT * FROM Cross_Border_Transactions;
    """
    rows = session.execute(query)
    return list(rows)
