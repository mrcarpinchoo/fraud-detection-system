# core modules
from typing import List

# third-party modules
from bson import ObjectId
from pydantic import BaseModel, Field

class Customer(BaseModel):
    id: str = Field(default_factory = lambda: str(ObjectId()), alias="_id")

    customer_name: str = Field(...)
    customer_email: str = Field(...)
    customer_accounts: List[str] = Field(..., description = "List of account_numbers.")

    class Config:
        allow_population_by_field_name = True
    # end class
# end class