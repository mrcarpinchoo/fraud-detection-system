#!/usr/bin/env python3

import json
from pymongo import MongoClient
from datetime import datetime, timedelta
import random
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

client = MongoClient("mongodb://localhost:27017")
db = client["iteso"]

# Helper Functions
def generateAccountNumber():
    return ''.join([str(random.randint(0, 9)) for _ in range(16)])

def generateAccountExpirationDate():
    return (datetime.now() + timedelta(days=30)).date().strftime('%Y-%m-%d')

# Models
class Account(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    customer_email: str = Field(...)
    account_number: str = Field(default_factory=generateAccountNumber)
    account_balance: float = Field(default=0.0)
    account_expiration_date: str = Field(default_factory=generateAccountExpirationDate)

    class Config:
        allow_population_by_field_name = True

class Customer(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    customer_name: str = Field(...)
    customer_email: str = Field(...)
    customer_accounts: List[str] = Field(..., description="List of account_numbers.")

    class Config:
        allow_population_by_field_name = True

class Transaction(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    customer_email: str = Field(...)
    account_number: str = Field(...)
    transaction_type: str = Field(...)
    transaction_amount: float = Field(..., ge=0)
    transaction_timestamp: datetime = Field(default_factory=datetime.now)
    transaction_details: Optional[Dict] = Field(default=None)

    class Config:
        allow_population_by_field_name = True

# Function to insert customer data
def insert_customer(customer_data):
    customer = Customer(**customer_data)
    db.customers.insert_one(customer.dict(by_alias=True))

# Function to insert account data
def insert_account(account_data):
    account = Account(**account_data)
    db.accounts.insert_one(account.dict(by_alias=True))

# Function to insert transaction data
def insert_transaction(transaction_data):
    transaction = Transaction(**transaction_data)
    db.transactions.insert_one(transaction.dict(by_alias=True))

# Read JSON data from files
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Helper function to generate random transactions
def generate_transaction(customer_email, account_number):
    transaction_type = random.choice(["deposit", "withdrawal", "transfer"])
    transaction_amount = random.uniform(10, 1000)  # Random amount between 10 and 1000
    transaction_details = {}

    if transaction_type == "withdrawal":
        transaction_details = {
            "withdrawal_method": random.choice(["ATM", "cashier"])
        }
    elif transaction_type == "transfer":
        transaction_details = {
            "payer_account_number": account_number,
            "beneficiary_account_number": generateAccountNumber(),
            "transfer_concept": random.choice(["payment", "gift", "services"])
        }
    
    transaction_data = {
        "customer_email": customer_email,
        "account_number": account_number,
        "transaction_type": transaction_type,
        "transaction_amount": transaction_amount,
        "transaction_details": transaction_details
    }
    
    insert_transaction(transaction_data)

# Function to generate data and insert it into MongoDB
def load_data_from_json():
    # Load customer data
    customer_data_list = read_json_file("data/customers.json")
    
    for customer_data in customer_data_list:
        # Insert customer into DB
        insert_customer(customer_data)

        # Generate 1 to 3 accounts per customer (randomly)
        account_data_list = []
        for _ in range(random.randint(1, 3)):  # Each customer can have 1 to 3 accounts
            account_data = {
                "customer_email": customer_data["customer_email"],
                "account_number": generateAccountNumber(),
                "account_balance": random.uniform(100, 5000),  # Random balance between 100 and 5000
                "account_expiration_date": generateAccountExpirationDate()
            }
            account_data_list.append(account_data)
            insert_account(account_data)

        # Update customer with the generated account numbers
        account_numbers = [account["account_number"] for account in account_data_list]
        db.customers.update_one(
            {"customer_email": customer_data["customer_email"]},
            {"$set": {"customer_accounts": account_numbers}}
        )

        # Generate 5 to 10 transactions for each customer
        for account_data in account_data_list:
            for _ in range(random.randint(5, 10)):  # Generate 5 to 10 transactions per account
                generate_transaction(customer_data["customer_email"], account_data["account_number"])

    print("Data loaded successfully!")

# Run the data loading process
load_data_from_json()
