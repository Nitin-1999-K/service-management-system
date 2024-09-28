from pydantic import BaseModel


class CustomerBase(BaseModel):
    name: str
    contact_number: str


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    id: int


class CustomerUpdate(BaseModel):
    name: str | None = None
    contact_number: str | None = None

