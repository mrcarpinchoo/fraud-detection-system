# third-party modules
from fastapi import APIRouter, Body, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder

# custom modules
from mongodb.src.model.Customer import Customer

router = APIRouter()

@router.get(
    "/{customer_email}",
    response_model = Customer,
    response_description = "Retrieves a single customer by email.",
    status_code = status.HTTP_200_OK
)
def getCustomerByEmail(customer_email: str, request: Request):
    try:
        result = request.app.database["customers"].find_one({ "customer_email": customer_email })

        if not result: raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Customer with email {customer_email} does not exist."
        )
        # end if

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

        if not result: raise Exception("Failed to create customer.")
        # end if
        
        return request.app.database["customers"].find_one({"_id": result.inserted_id}) # returns customer object
    except Exception as e: raise HTTPException(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail = f"Internal server error: {e}"
    )
# end def