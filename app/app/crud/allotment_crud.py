
from sqlalchemy.orm import Session
from schemas import AllotmentCreate
from models import Ticket as TicketModel, TicketAllotment as TicketAllotmentModel


def allotTicket(db: Session, allotment: AllotmentCreate, allocator_id: str, db_ticket: TicketModel):
    db.add(TicketAllotmentModel(**allotment.model_dump(), allocator_id = allocator_id))
    db_ticket.status_code = 1
    db.commit()


# def reallotTicker(db: Session, )

def getAllotmentById(
    db: Session,
    allotment_id: int,
    status_codes: list[int] | None = None
):
    if status_codes:
        allotment = db.query(TicketAllotmentModel).filter(TicketAllotmentModel.id == allotment_id, 
                                                          TicketAllotmentModel.status_codes.in_(status_codes)).first()
    else:
        allotment = db.query(TicketAllotmentModel).filter(TicketAllotmentModel.id == allotment_id).first()
    return allotment


def findLatestAllotment(
    db: Session,
    ticket_id: int,
    status_codes: list[int] | None = None
):
    if status_codes:
        allotment = db.query(TicketAllotmentModel).filter(
        TicketAllotmentModel.ticket_id == ticket_id,
        TicketAllotmentModel.status_code.in_(status_codes)).order_by(TicketAllotmentModel.id.desc()).first()
    else:
        allotment = db.query(TicketAllotmentModel).filter(
        TicketAllotmentModel.ticket_id == ticket_id).order_by(TicketAllotmentModel.id.desc()).first()
    return allotment

