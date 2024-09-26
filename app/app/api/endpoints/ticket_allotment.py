from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from crud import allotment_crud
from schemas import AllotmentCreate, AllotmentRevise
from models import User as UserModel
from api import deps
from crud import user_crud, ticket_crud


def allotTicket(
    allotment: AllotmentCreate, 
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_head)
):
    
    engineer = user_crud.getUserById(db = db, user_id = allotment.engineer_id, status_code = 1)

    if not engineer:
        raise HTTPException(404, "Engineer not found")
    
    if engineer.user_type != 3:
        raise HTTPException(409, "Ticket can be alloted only to an engineer")
        
    if current_user.user_type == 2 and engineer.supervisor_id != current_user.id:
        raise HTTPException(403, "Engineer is not under the supervision of the current user")
    
    db_ticket = ticket_crud.getTicketById(db = db, ticket_id = allotment.ticket_id, status_codes = [0,1])
    
    if not db_ticket:
        raise HTTPException(404, "Ticket not found")
    
    if db_ticket.status_code == 1:
        raise HTTPException(409, "Ticket Already Alloted to an engineer")
    
    allotment_crud.allotTicket(db = db, allotment = allotment, allocator_id = current_user.id, db_ticket = db_ticket)


def reviseAllotment(
    allotment_revise: AllotmentRevise,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_head)   
):
    ticket = ticket_crud.getTicketById(db = db, ticket_id = AllotmentRevise.ticket_id, status_codes = [0,1]).first()

    if not ticket:
        raise HTTPException(404, "Ticket not found")
    
    if ticket.status_code == 0:
        raise HTTPException(404, "Ticket is not alloted to anyone")

    # allotment_prev = allotment_crud.findLatestAllotment(db = db, ticket_id = allotment_revise.ticket_id)

    allotment_prev = ticket.all
    
    if not allotment_prev: # This is only for double checking eventhough I already checked if ticket.status_code == 0
        raise HTTPException(404, "Ticket is not alloted to anyone")
    
    if allotment_prev.status_code == 3: # This is only for double checking eventhough I already checked if ticket.status_code == 0
        raise HTTPException(404, "Ticket is not alloted to anyone")

    if allotment_prev.status_code == 1:
        raise HTTPException(409, "Service engineer already departed")
    
    # Cancelled => -1, Pending => 0, Departed => 1, Re-assigned => 2 Released => 3

    engineer = user_crud.getUserById(db = db, user_id = allotment_revise.engineer_id, status_code = 1)

    if not engineer:
        raise HTTPException(404, "Engineer not found")

    if engineer.user_type != 3:
        raise HTTPException(409, "Ticket can be alloted only to an engineer")

    if current_user.user_type == 2:

        if allotment_prev.engineer.supervisor_id != current_user.id:
            raise HTTPException(403, "This ticket is not under the control of current service head")
        
        if engineer.supervisor_id != current_user.id:
            raise HTTPException(403, "Engineer is not under the supervision of the current user")

    allotment_crud.reviseAllotment()

# Change old ticket status to re-assigned



# def releaseTicket()
# onboarded and cancelled tickets cannot be released
# change back to pending after release