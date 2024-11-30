from model import (
    connect_to_cassandra,
    create_keyspace,
    create_tables,
    bulk_insert_from_json,
    query_recent_transactions,
    query_anomalies,
    query_withdrawals,
    query_login_attempts,
    query_cross_border_transactions,
)
from config import KEYSPACE
import json


def main():
    # Connect to Cassandra
    session = connect_to_cassandra()
    print("Connected to Cassandra.")

    # Create keyspace and tables
    create_keyspace(session)
    print(f"Keyspace '{KEYSPACE}' ensured.")

    create_tables(session)
    print("Tables created.")

    # Load and insert bulk data from JSON
    with open("example_data.json", "r") as file:
        data = json.load(file)
        bulk_insert_from_json(session, data)
    print("Bulk data inserted from 'example_data.json'.")

    # Query data
    print("\nQuerying data for demonstration:")

    # 1. Query Recent Transactions
    print("\nRecent Transactions:")
    for row in query_recent_transactions(session, limit=5):
        print(row)

    # 2. Query Anomalies
    print("\nAnomaly Detection Results:")
    for row in query_anomalies(session):
        print(row)

    # 3. Query Anomalies
    print("\nAnomaly Detection Results:")
    for row in query_withdrawals(session):
        print(row)

    # 4. Query Customer Login Attempts
    print("\nCustomer Login Attempts:")
    for row in query_login_attempts(session, limit=5):
        print(row)

    # 5. Query Cross-Border Transactions
    print("\nCross-Border Transactions:")
    for row in query_cross_border_transactions(session):
        print(row)

    # Clean up
    session.shutdown()
    print("Cassandra session closed.")


if __name__ == "__main__":
    main()
