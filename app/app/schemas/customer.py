from pydantic import BaseModel


class CustomerCreate(BaseModel):
    name: str
    contact_number: str
