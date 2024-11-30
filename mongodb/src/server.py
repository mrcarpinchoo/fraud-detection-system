#!/usr/bin/env python3

# third-party modules
from fastapi import FastAPI

# custom modules
import mongodb.db.connection as conn
import mongodb.src.router.customer as customerRouter
import mongodb.src.router.account as accountRouter
import mongodb.src.router.transaction as transactionRouter

app = FastAPI() # starts a FastAPI application

@app.on_event("startup")
def startupDBClient():
    app.database = None

    try:
        # MongoDB client connection
        app.mongoClient = conn.mongoClient
        app.database = conn.database
        
        app.mongoClient.admin.command('ping') # tests connection by pinging the server

        print("Connected to MongoDB successfully!")
    except Exception as e: print(f"Failed to connect to MongoDB: {e}")

    try:
        # customers indexes
        app.database["customers"].create_index("customer_email", unique = True)

        # accounts indexes
        app.database["accounts"].create_index("customer_email")
        app.database["accounts"].create_index("account_number", unique = True)

        # transactions indexes
        app.database["transactions"].create_index("account_number")
        app.database["transactions"].create_index("transaction_type")
    except Exception as e: print(f"Failed to create indexes: {e}")
# end def

@app.on_event("shutdown")
def shutdownDBClient():
    app.mongoClient.close() # closes MongoDB client connection

    print("Disconnected from MongoDB")
# end def

app.include_router(customerRouter.router, tags = ["customer"], prefix = "/api/customers") # includes the /api/customers APIRouter in the same current APIRouter
app.include_router(accountRouter.router, tags = ["accounts"], prefix = "/api/accounts") # includes the /api/accounts APIRouter in the same current APIRouter
app.include_router(transactionRouter.router, tags = ["transactions"], prefix = "/api/transactions") # includes the api/transactions APIRouter in the same current APIRouter