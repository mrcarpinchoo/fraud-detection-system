from model import connect_to_cassandra, create_keyspace, create_tables, insert_example_data, query_recent_transactions, query_anomalies, query_login_attempts, query_cross_border_transactions
from config import KEYSPACE

def main():
    # Connect to Cassandra
    session = connect_to_cassandra()
    print("Connected to Cassandra.")

    # Create keyspace and tables
    create_keyspace(session)
    print(f"Keyspace '{KEYSPACE}' ensured.")

    create_tables(session)
    print("Tables created.")

    # Insert example data
    account_id, customer_id = insert_example_data(session)
    print(f"Example data inserted for account ID: {account_id} and customer ID: {customer_id}")

    # Query data
    # 1. Query Recent Transactions
    print("\nRecent Transactions:")
    recent_transactions = query_recent_transactions(session, account_id, limit=5)
    for row in recent_transactions:
        print(row)

    # 2. Query Anomalies
    print("\nAnomaly Detection Results:")
    anomalies = query_anomalies(session, account_id)
    for row in anomalies:
        print(row)

    # 3. Query Customer Login Attempts
    print("\nCustomer Login Attempts:")
    login_attempts = query_login_attempts(session, customer_id, limit=5)
    for row in login_attempts:
        print(row)

    # 4. Query Cross-Border Transactions
    print("\nCross-Border Transactions:")
    cross_border_transactions = query_cross_border_transactions(session, account_id)
    for row in cross_border_transactions:
        print(row)

    # Clean up
    session.shutdown()
    print("Cassandra session closed.")

if __name__ == "__main__":
    main()
