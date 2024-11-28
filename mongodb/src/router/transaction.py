# core modules

# third-party modules
from fastapi import APIRouter, Body, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder

# custom modules
from mongodb.src.model.Transaction import Transaction

router = APIRouter()

@router.post(
    "/",
    response_model = Transaction,
    response_description = "Performs a new transaction.",
    status_code = status.HTTP_201_CREATED
)
def performTransaction(request: Request, transaction: Transaction = Body(...)):
    transactionType = transaction.transactionType
    try:
        if transactionType == "deposit":
            transactionResult = request.app.database["transactions"].insert_one(jsonable_encoder(transaction))

            if not transactionResult: raise Exception("Failed to perform transaction.")
            # end if

            selection = {
                "email": transaction.customer_email,
                "accounts.number": transaction.account_number
            }

            updateOperation = { "$inc": { "accounts.$.balance": transaction.amount } }

            updateResult = request.app.database["customers"].update_one(selection, updateOperation)

            if not updateResult: raise Exception("Failed to update account balance.")
            # end if
            
            return request.app.database["transactions"].find_one({"_id": transactionResult.inserted_id}) # returns customer object
        elif transactionType == "withdrawal":
            pass
        elif transactionType == "transfer":
            pass
        # end if-elif
    except Exception as e: raise HTTPException(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail = f"Internal server error: {e}"
    )
# end def