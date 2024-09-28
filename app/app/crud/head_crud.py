from sqlalchemy import or_
from sqlalchemy.orm import Session
from schemas import Allotment
from models import User as UserModel, Ticket as TicketModel, TicketAllotment as TicketAllotmentModel, TicketProgress as TicketProgressModel



def getPendingTickets(
    db: Session,
    supervisor_id: str
):
    return (
        db.query(TicketModel)
        .outerjoin(TicketAllotmentModel)
        .join(UserModel, UserModel.id == TicketAllotmentModel.engineer_id)
        .outerjoin(TicketProgressModel, TicketProgressModel.allotment_id == TicketAllotmentModel.id)
        .filter(
            UserModel.supervisor_id == supervisor_id,
            or_(TicketAllotmentModel.status_code == 0,
                TicketProgressModel.status_code == 0)
                )
        .all()
    )