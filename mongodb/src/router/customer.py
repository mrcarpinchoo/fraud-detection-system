# core modules

# third-party modules
from fastapi import APIRouter, Body, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder

# custom modules
from mongodb.src.model.Customer import Customer, Account

router = APIRouter()

@router.get(
    "/{email}",
    response_model = Customer,
    response_description = "Retrieves a single customer by email.",
    status_code = status.HTTP_200_OK
)
def getCustomerByEmail(email: str, request: Request):
    try:
        result = request.app.database["customers"].find_one({ "email": email })

        if not result: raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Customer with email {email} does not exist."
        )

        return result
    except HTTPException as e: raise e
    except Exception as e: raise HTTPException(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail = f"Internal server error: {e}"
    )
# end def

@router.post(
    "/",
    response_model = Customer,
    response_description = "Creates a new customer.",
    status_code = status.HTTP_201_CREATED
)
def createCustomer(request: Request, customer: Customer = Body(...)):
    try:
        result = request.app.database["customers"].insert_one(jsonable_encoder(customer))

        if not result: raise Exception("Failed to create new customer.")
        # end if
        
        return request.app.database["customers"].find_one({"_id": result.inserted_id}) # returns customer object
    except Exception as e: raise HTTPException(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail = f"Internal server error: {e}"
    )
# end def

@router.put(
    "/{id}/accounts",
    response_model = Account,
    response_description = "Creates new customer account.",
    status_code = status.HTTP_200_OK
)
def createAccount(id: str, request: Request, account: Account = Body(...)):
    selection = { "_id": id }

    updateOperation = { "$push": { "accounts": jsonable_encoder(account) } }

    try:
        result = request.app.database["customers"].update_one(selection, updateOperation)

        if result.matched_count == 0: raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Customer with ID {id} does not exist."
        )
        # end if

        return result.raw_result # returns the account embedded document
    except HTTPException as e: raise e
    except Exception as e: raise HTTPException(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail = f"Internal server error: {e}"
    )
# end def