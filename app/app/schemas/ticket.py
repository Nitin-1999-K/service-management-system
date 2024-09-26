from pydantic import BaseModel


class TicketCreate(BaseModel):
    description: str
    branch_location: str
    customer_id: str