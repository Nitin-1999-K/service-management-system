from .user import *
from .customer import *
from .ticket import *
from .ticket_allotment import *
from .ticket_progress import *
from pydantic import BaseModel


class Message(BaseModel):
    detail: str
