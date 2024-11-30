# third-party modules
from fastapi import APIRouter, Body, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder

# custom modules
from mongodb.src.model.Transaction import Transaction

router = APIRouter()

@router.get(
    "/{account_number}/summary",
    # response_model = Customer,
    response_description = "",
    status_code = status.HTTP_200_OK
)
def getTransactionSummary(account_number: str, request: Request):
    pipeline = [
        {
            "$match": {
                "account_number": account_number,
                "transaction_type": { "$in": [ "deposit", "withdrawal" ] }
            }
        },
        {
            "$group": {
                "_id": "$transaction_type",
                "total_amount": { "$sum": "$transaction_amount" }
            }
        }
    ]

    try:
        result = request.app.database["transactions"].aggregate(pipeline)

        if not result: raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Account with number {account_number} does not exist."
        )
        # end if

        return list(result)
    except HTTPException as e: raise e
    except Exception as e: raise HTTPException(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail = f"Internal server error: {e}"
    )
# end def

@router.post(
    "/",
    response_model = Transaction,
    response_description = "Performs a new transaction.",
    status_code = status.HTTP_201_CREATED
)
def performTransaction(request: Request, transaction: Transaction = Body(...)):
    transactionType = transaction.transaction_type

    try:
        transactionResult = request.app.database["transactions"].insert_one(jsonable_encoder(transaction))
            
        if not transactionResult: raise Exception(f"Failed to perform {transactionType}.")
        # end if

        if transactionType in ["deposit", "withdrawal"]:
            selection = { "account_number": transaction.account_number }

            updateOperation = { 
                "$inc": { 
                    "account_balance": transaction.transaction_amount
                        if transactionType == "deposit"
                        else -transaction.transaction_amount
                }
            }

            updateBalanceResult = request.app.database["accounts"].update_one(selection, updateOperation) # increases or decreases the account balance

            if not updateBalanceResult: raise Exception("Failed to update account balance.")
            # end if
        elif transactionType == "transfer":
            # updating payer account
            payerSelection = { "account_number": transaction.transaction_details["payer_account_number"] }

            payerUpdateOperation = { "$inc": { "account_balance": -transaction.transaction_amount } }

            updateBalanceResult = request.app.database["accounts"].update_one(payerSelection, payerUpdateOperation) # increases or decreases the account balance

            if not updateBalanceResult: raise Exception("Failed to update payer account balance.")

            # updating beneficiary account
            beneficiarySelection = { "account_number": transaction.transaction_details["beneficiary_account_number"] }

            beneficiaryUpdateOperation = { "$inc": { "account_balance": transaction.transaction_amount } }

            updateBalanceResult = request.app.database["accounts"].update_one(beneficiarySelection, beneficiaryUpdateOperation) # increases or decreases the account balance

            if not updateBalanceResult: raise Exception("Failed to update beneficiary account balance.")
        # end if-elif

        return request.app.database["transactions"].find_one({"_id": transactionResult.inserted_id}) # returns transaction object
    except Exception as e: raise HTTPException(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail = f"Internal server error: {e}"
    )
# end def