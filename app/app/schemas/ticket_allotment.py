from pydantic import BaseModel


class Allotment(BaseModel):
    ticket_id: int
    engineer_id: str
    

class AllotmentCreate(Allotment):
    pass


class AllotmentRevise(Allotment):
    pass