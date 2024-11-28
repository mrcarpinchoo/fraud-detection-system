# core modules
from datetime import datetime
from typing import Dict, Optional

# third-party modules
from bson import ObjectId
from pydantic import BaseModel, Field

class Transaction(BaseModel):
    id: str = Field(default_factory = lambda: str(ObjectId()), alias="_id")
    customer_email: str = Field(..., description = "Customer email address related to the transaction.")
    account_number: str = Field(..., description = "Account number related to the transaction.")
    transactionType: str = Field(...)
    amount: float = Field(..., ge = 0)
    timestamp: datetime = Field(default_factory = datetime.now)
    details: Optional[Dict] = Field(default = None)

    class Config:
        allow_population_by_field_name = True
# end class
