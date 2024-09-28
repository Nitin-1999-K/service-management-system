from db.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Customer(Base):

    id = Column(Integer, primary_key=True)
    name = Column(String(20), index=True, nullable=False)
    contact_number = Column(String(10), unique=True, nullable=False)

    ticket = relationship("Ticket", back_populates="customer")
