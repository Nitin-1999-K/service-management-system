from pydantic import BaseModel
from datetime import datetime


class Allotment(BaseModel):
    ticket_id: int
    engineer_id: str


class AllotmentCreate(Allotment):
    pass


class AllotmentRevise(Allotment):
    pass


class AllotmentResponse(Allotment):
    id: int
    allocator_id: str 
    alloted_datetime: datetime
    status_code: int