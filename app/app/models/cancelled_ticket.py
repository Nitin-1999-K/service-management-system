from db.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship


class CancelledTicket(Base):

    __tablename__ = "cancelled_ticket"

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey("ticket.id"))
    user_id = Column(String(20), ForeignKey("user.id"))
    description = Column(String(255), nullable=False)
    cancelled_datetime = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="cancelled_ticket")
    ticket = relationship("Ticket", back_populates="cancelled_ticket")
