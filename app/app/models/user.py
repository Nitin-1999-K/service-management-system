from db.db import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship


class User(Base):

    __tablename__ = "user"  # Self join requires table name to be explicitly declared

    id = Column(String(20), primary_key=True)
    user_type = Column(Integer, nullable=False)
    full_name = Column(String(20), index=True, nullable=False)
    email = Column(String(30), unique=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    mobile_number = Column(String(10), unique=True, nullable=False)
    status_code = Column(Integer, default=1)
    created_datetime = Column(DateTime, default=datetime.utcnow())

    supervisor_id = Column(String(20), ForeignKey("user.id"))

    supervisor = relationship("User", remote_side=[id], backref="subordinate")
    ticket = relationship(
        "Ticket", secondary="ticket_raiser", back_populates="raised_by"
    )
    assigned_allotment = relationship(
        "TicketAllotment",
        foreign_keys="TicketAllotment.allocator_id",
        back_populates="allocator",
    )
    received_allotment = relationship(
        "TicketAllotment",
        foreign_keys="TicketAllotment.engineer_id",
        back_populates="engineer",
    )
    cancelled_ticket = relationship("CancelledTicket", back_populates="user")

    def __init__(
        self,
        user_type,
        full_name,
        email,
        hashed_password,
        mobile_number,
        supervisor_id,
        db,
    ):

        self.user_type = user_type
        self.full_name = full_name
        self.email = email
        self.hashed_password = hashed_password
        self.mobile_number = mobile_number
        self.supervisor_id = supervisor_id

        max_id = db.query(User.id).order_by(User.id.desc()).first()

        if not max_id:
            self.id = f"EMP{1:03d}"
        else:
            self.id = f"EMP{int(max_id[0][3:]) + 1:03d}"
