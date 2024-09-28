from db.db import Base
from sqlalchemy import Column, Integer, ForeignKey, String


class TicketRaiser(Base):

    __tablename__ = "ticket_raiser"

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey("ticket.id"))
    user_id = Column(String(20), ForeignKey("user.id"))
