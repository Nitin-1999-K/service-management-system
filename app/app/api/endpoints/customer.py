from fastapi import APIRouter, Depends
from api import deps
from sqlalchemy.orm import Session
from models import User as UserModel
from schemas import CustomerCreate, TicketCreate
from crud import customer_crud, ticket_crud
from endpoints import ticket

router = APIRouter()


@router.post("/")
def addCustomer(
    customer: CustomerCreate,
    db: Session = Depends(deps.get_db),
    user: UserModel = Depends(deps.get_current_head)
):
    customer_crud.addCustomer(db = db, customer= customer)


@router.post("/ticket")
def raiseTicket(
    ticket_create: TicketCreate,
    db: Session = Depends(deps.get_db)
):
    return ticket.raiseTicket(db = db, ticket_create = ticket_create, current_user = None)


# Customer can delete ticket only if the status is in pending condition