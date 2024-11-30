from model import (
    connect_to_cassandra,
    create_keyspace,
    create_tables,
    bulk_insert_from_json,
    query_recent_transactions,
    query_anomalies,
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
    # Replace with IDs present in your JSON data for testing
    test_account_id = uuid.UUID(data["accounts"][0]["account_id"])
    test_customer_id = uuid.UUID(data["customers"][0]["customer_id"])

    # 1. Query Recent Transactions
    print("\nRecent Transactions:")
    recent_transactions = query_recent_transactions(session, test_account_id, limit=5)
    for row in recent_transactions:
        print(row)

    # 2. Query Anomalies
    print("\nAnomaly Detection Results:")
    anomalies = query_anomalies(session, test_account_id)
    for row in anomalies:
        print(row)

    # 3. Query Customer Login Attempts
    print("\nCustomer Login Attempts:")
    login_attempts = query_login_attempts(session, test_customer_id, limit=5)
    for row in login_attempts:
        print(row)

    # 4. Query Cross-Border Transactions
    print("\nCross-Border Transactions:")
    cross_border_transactions = query_cross_border_transactions(session, test_account_id)
    for row in cross_border_transactions:
        print(row)

    # Clean up
    session.shutdown()
    print("Cassandra session closed.")


if __name__ == "__main__":
    main()
