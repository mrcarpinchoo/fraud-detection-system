# core modules
from datetime import datetime, timedelta
import random

# third-party modules
from bson import ObjectId
from pydantic import BaseModel, Field

def generateAccountNumber():
    return ''.join([str(random.randint(0, 9)) for _ in range(16)])
# end def

def generateAccountExpirationDate():
    return (datetime.now() + timedelta(days = 30)).date() # generates account expiration date 30 days after creation date
# end def

class Account(BaseModel):
    id: str = Field(default_factory = lambda: str(ObjectId()), alias="_id")

    customer_email: str = Field(...)

    account_number: str = Field(default_factory = generateAccountNumber)
    account_balance: float = Field(default = 0.0)
    account_expiration_date: str = Field(default_factory = generateAccountExpirationDate)

    class Config:
        allow_population_by_field_name = True
    # end class
# end class