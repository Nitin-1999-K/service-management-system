from pydantic import BaseModel
from datetime import datetime

class TicketBase(BaseModel):
    description: str
    branch_location: str


class TicketCreate(TicketBase):
    customer_id: int    


class TicketResponse(TicketBase):
    id: int
    created_datetime: datetime
    