from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement
import uuid
from datetime import datetime
from config import CASSANDRA_HOSTS, CASSANDRA_PORT, KEYSPACE


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
            timestamp timestamp,
            transaction_id uuid,
            amount decimal,
            transaction_type text,
            location text,
            PRIMARY KEY (account_id, timestamp)
        ) WITH CLUSTERING ORDER BY (timestamp DESC);
        """,
        """
        CREATE TABLE IF NOT EXISTS Anomaly_Detection (
            account_id uuid,
            timestamp timestamp,
            transaction_id uuid,
            anomaly_type text,
            anomaly_score int,
            PRIMARY KEY (account_id, timestamp)
        ) WITH CLUSTERING ORDER BY (timestamp DESC);
        """,
        """
        CREATE TABLE IF NOT EXISTS Frequent_Withdrawals (
            account_id uuid,
            timestamp timestamp,
            transaction_id uuid,
            amount decimal,
            PRIMARY KEY (account_id, timestamp)
        ) WITH CLUSTERING ORDER BY (timestamp DESC);
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
            timestamp timestamp,
            transaction_id uuid,
            foreign_location text,
            amount decimal,
            PRIMARY KEY (account_id, timestamp)
        ) WITH CLUSTERING ORDER BY (timestamp DESC);
        """
    ]

    for table_cql in tables:
        session.execute(table_cql)

# =======================
# Insert Example Data
# =======================

def insert_example_data(session):
    session.set_keyspace(KEYSPACE)

    account_id = uuid.uuid4()
    customer_id = uuid.uuid4()

    # Insert transaction history
    for i in range(3):
        insert_transaction_history(session, account_id, 1000 + i * 100, 'deposit', 'New York, USA')

    # Insert anomaly detection data
    session.execute("""
    INSERT INTO Anomaly_Detection (account_id, timestamp, transaction_id, anomaly_type, anomaly_score)
    VALUES (%s, %s, %s, %s, %s);
    """, (account_id, datetime.now(), uuid.uuid4(), 'suspicious_pattern', 85))

    # Insert frequent withdrawals
    session.execute("""
    INSERT INTO Frequent_Withdrawals (account_id, timestamp, transaction_id, amount)
    VALUES (%s, %s, %s, %s);
    """, (account_id, datetime.now(), uuid.uuid4(), 3000))

    # Insert login history
    session.execute("""
    INSERT INTO Customer_Login_History (customer_id, login_timestamp, ip_address, login_success)
    VALUES (%s, %s, %s, %s);
    """, (customer_id, datetime.now(), '192.168.0.1', True))

    # Insert cross-border transaction
    session.execute("""
    INSERT INTO Cross_Border_Transactions (account_id, timestamp, transaction_id, foreign_location, amount)
    VALUES (%s, %s, %s, %s, %s);
    """, (account_id, datetime.now(), uuid.uuid4(), 'Tokyo, Japan', 5000))

    return account_id, customer_id

# =======================
# Helper Insert Functions
# =======================

def insert_transaction_history(session, account_id, amount, transaction_type, location):
    insert_cql = """
    INSERT INTO Transaction_History (account_id, timestamp, transaction_id, amount, transaction_type, location)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    transaction_id = uuid.uuid4()
    session.execute(insert_cql, (
        account_id,
        datetime.now(),
        transaction_id,
        amount,
        transaction_type,
        location
    ))

# =======================
# Query Functions
# =======================

def query_recent_transactions(session, account_id, limit=10):
    query = """
    SELECT * FROM Transaction_History
    WHERE account_id = %s
    LIMIT %s;
    """
    rows = session.execute(query, (account_id, limit))
    return list(rows)


def query_anomalies(session, account_id):
    query = """
    SELECT * FROM Anomaly_Detection
    WHERE account_id = %s;
    """
    rows = session.execute(query, (account_id,))
    return list(rows)


def query_login_attempts(session, customer_id, limit=5):
    query = """
    SELECT * FROM Customer_Login_History
    WHERE customer_id = %s
    LIMIT %s;
    """
    rows = session.execute(query, (customer_id, limit))
    return list(rows)


def query_cross_border_transactions(session, account_id):
    query = """
    SELECT * FROM Cross_Border_Transactions
    WHERE account_id = %s;
    """
    rows = session.execute(query, (account_id,))
    return list(rows)
