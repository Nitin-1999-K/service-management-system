from sqlalchemy import or_
from sqlalchemy.orm import Session
from schemas import Allotment
from models import Ticket as TicketModel, TicketAllotment as TicketAllotmentModel, TicketProgress as TicketProgressModel


def getTickets(
    db: Session, engineer_id: str, status_codes: list[int] | None = None
):

    if status_codes:
        return (
            db.query(TicketAllotmentModel)
            .filter(
                TicketAllotmentModel.engineer_id == engineer_id,
                TicketAllotmentModel.status_code.in_(status_codes),
            )
            .order_by(TicketAllotmentModel.ticket_id)
            .all()
        )

    return (
        db.query(TicketAllotmentModel)
        .filter(TicketAllotmentModel.engineer_id == engineer_id)
        .order_by(TicketAllotmentModel.ticket_id)
        .all()
    )


def getTicket(db: Session, engineer_id: str, ticket_id: int):
    return (
        db.query(TicketAllotmentModel)
        .filter(
            TicketAllotmentModel.engineer_id == engineer_id,
            TicketAllotmentModel.ticket_id == ticket_id,
        )
        .all()
    )


def getPendingTickets(
    db: Session,
    engineer_id: str
):
    return (
        db.query(TicketModel)
        .outerjoin(TicketAllotmentModel)
        .outerjoin(TicketProgressModel)
        .filter(
            TicketAllotmentModel.engineer_id == engineer_id,
            or_(TicketAllotmentModel.status_code == 0,
                TicketProgressModel.status_code == 0)
                )
        .all()
    )