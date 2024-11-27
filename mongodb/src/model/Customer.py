# core modules
from datetime import datetime, timedelta
import random
from typing import List
import uuid

# third-party modules
from pydantic import BaseModel, Field

def generateAccountNumber() -> str:
    return ''.join([str(random.randint(0, 9)) for _ in range(16)])
# end def

def generateAccountExpirationDate():
    return (datetime.now() + timedelta(days = 30)).date() # generates account expiration date 30 days after creation date
# end def

class Account(BaseModel):
    id: str = Field(default_factory = uuid.uuid4, alias = "_id")
    number: str = Field(default_factory = generateAccountNumber)
    balance: float = Field(default = 0.0)
    expiration_date: str = Field(default_factory = generateAccountExpirationDate)

    class Config:
        allow_population_by_field_name = True
    # end class
# end class

class Customer(BaseModel):
    id: str = Field(default_factory = uuid.uuid4, alias = "_id")
    name: str = Field(...)
    email: str = Field(...)
    accounts: List[Account] = Field(...)

    class Config:
        allow_population_by_field_name = True
    # end class
# end class