# core modules
from datetime import datetime
from typing import Dict, Optional

# third-party modules
from bson import ObjectId
from pydantic import BaseModel, Field

class Transaction(BaseModel):
    id: str = Field(default_factory = lambda: str(ObjectId()), alias="_id")

    customer_email: str = Field(..., description = "Email address of the customer who performs the transaction.")
    account_number: str = Field(..., description = "Account number that performs the transaction.")

    transaction_type: str = Field(..., description = "Type of transaction (deposit, withdrawal, or transfer).")
    transaction_amount: float = Field(..., ge = 0)
    transaction_timestamp: datetime = Field(default_factory = datetime.now)
    transaction_details: Optional[Dict] = Field(default = None, description = "Additional fields based on the type of transaction.")

    class Config:
        allow_population_by_field_name = True
# end class