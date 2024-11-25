# core modules

# third-party modules
from fastapi import APIRouter, Body, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder

# custom modules
from mongodb.src.model.Customer import Customer
# from mongodb.src.model.Transaction import Transaction

router = APIRouter()

@router.post(
    "/",
    response_model = Customer,
    status_code = status.HTTP_201_CREATED
)
def createCustomer(request: Request, customer: Customer = Body(...)):
    try:
        result = request.app.database["customers"].insert_one(jsonable_encoder(customer))
        
        return request.app.database["customers"].find_one({"_id": result.inserted_id}) # returns customer object
    except Exception as e: raise Exception(f"Error creating user: {e}")
# end def