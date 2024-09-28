from db.db import Base
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship


class TicketProgress(Base):

    __tablename__ = "ticket_progress"

    id = Column(Integer, primary_key=True)
    departed_datetime = Column(DateTime, default=func.now())
    description = Column(String(255))
    image_url = Column(String(100))
    initiated_datetime = Column(DateTime)
    status_code = Column(
        Integer, default=0
    )  # -1 => Cancelled 0 => Pending 1 => Initiated 2 => Completed
    priority = Column(Integer, default=1)  # 1 => Low, 2 => Medium, 3 => High
    expected_datetime = Column(DateTime)
    completed_datetime = Column(DateTime)

    allotment_id = Column(Integer, ForeignKey("ticket_allotment.id"))

    ticket_allotment = relationship("TicketAllotment", back_populates="ticket_progress")
