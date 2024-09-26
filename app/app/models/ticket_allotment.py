from db.db import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship


class TicketAllotment(Base):

    __tablename__ = "ticket_allotment"

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey("ticket.id"))
    allocator_id = Column(String(20), ForeignKey("user.id"))
    engineer_id = Column(String(20), ForeignKey("user.id")) # => See instagram chat

    alloted_datetime = Column(DateTime, default=datetime.utcnow())
    status_code = Column(Integer, default = 0) 
    # cancelled => -1, pending => 0, departed => 1, re-assigned => 2, released => 3

    ticket = relationship("Ticket", back_populates = "ticket_allotment")

    allocator = relationship('User', foreign_keys=[allocator_id], back_populates='assigned_allotment')
    engineer = relationship('User', foreign_keys=[engineer_id], back_populates='received_allotment') 