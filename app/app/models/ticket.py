from db.db import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship


class Ticket(Base):

    id = Column(Integer, primary_key=True)
    
    description = Column(String(100))
    image_path = Column(String(75), unique=True)
    branch_location = Column(String(75))
    created_datetime = Column(DateTime, default=datetime.utcnow())
    status_code = Column(Integer, default = 0) # Pending, Assigned, Cancelled 

    customer_id = Column(Integer, ForeignKey('customer.id'))

    customer = relationship("Customer", back_populates = "ticket")
    raised_by = relationship("User", secondary = "ticket_raiser", back_populates = "ticket", uselist = False)
    ticket_alloted = relationship("TicketAllotment", back_populates = "ticket")

    