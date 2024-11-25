# core modules
import uuid
from typing import List

# third-party modules
from pydantic import BaseModel, Field

class Account(BaseModel):
    id: str = Field(default_factory = uuid.uuid4, alias = "_id")
    number: str = Field(...)
    balance: float = Field(...)
    expiration_date: str = Field(...)

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