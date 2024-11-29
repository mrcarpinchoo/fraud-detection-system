# core modules
from typing import List

# third-party modules
from fastapi import APIRouter, Body, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder

# custom modules
from mongodb.src.model.Account import Account

router = APIRouter()

@router.get(
    "/{account_number}",
    response_model = Account,
    response_description = "Retrieves the account with the given the account number.",
    status_code = status.HTTP_200_OK
)
def getAccountByNumber(account_number: str, request: Request):
    try:
        result = request.app.database["accounts"].find_one({ "account_number": account_number })

        if not result: raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Account with email address {account_number} does not exist."
        )
        # end if

        return result
    except HTTPException as e: raise e
    except Exception as e: raise HTTPException(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail = f"Internal server error: {e}"
    )
# end def

@router.get(
    "/",
    response_model = List[Account],
    response_description = "Retrieves all the accounts with the given email address.",
    status_code = status.HTTP_200_OK
)
def getAccountsByEmail(customer_email: str, request: Request):
    try:
        cursor = request.app.database["accounts"].find({ "customer_email": customer_email })

        accounts = list(cursor) 

        if not accounts: raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Account with email address {customer_email} does not exist."
        )
        # end if

        return accounts
    except HTTPException as e: raise e
    except Exception as e: raise HTTPException(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail = f"Internal server error: {e}"
    )
# end def

@router.post(
    "/",
    response_model = Account,
    response_description = "Creates a new account.",
    status_code = status.HTTP_200_OK
)
def createAccount(request: Request, account: Account = Body(...)):
    try:
        result = request.app.database["accounts"].insert_one(jsonable_encoder(account))

        if not result: raise Exception("Failed to create account.")
        # end if
        
        return request.app.database["accounts"].find_one({"_id": result.inserted_id}) # returns account object
    except Exception as e: raise HTTPException(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail = f"Internal server error: {e}"
    )
# end def