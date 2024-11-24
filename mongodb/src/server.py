#!/usr/bin/env python3

# third-party modules
from fastapi import FastAPI

# custom modules
import mongodb.db.connection as conn
import mongodb.src.router.customer as customerRouter
import mongodb.src.router.transaction as transactionRouter

app = FastAPI() # starts a FastAPI application

@app.on_event("startup")
def startupDBClient():
    # MongoDB client connection
    app.mongoClient = conn.mongoClient 
    app.database = conn.database

    print("Connected to MongoDB successfully!")
# end def

@app.on_event("shutdown")
def shutdownDBClient():
    app.mongoClient.close() # closes MongoDB client connection

    print("Disconnected from MongoDB")
# end def

app.include_router(customerRouter.router, tags = ["customer"], prefix = "/api/customers") # includes the /api/customers APIRouter in the same current APIRouter
app.include_router(transactionRouter.router, tags = ["transactions"], prefix = "/api/transactions") # includes the api/transactions APIRouter in the same current APIRouter