from fastapi import APIRouter

from .endpoints import (
    admin,
    head,
    login,
    ticket,
    customer,
    ticket_allotment,
    ticket_progress,
    user,
    customer,
    engineer
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"], prefix="/login")
api_router.include_router(admin.router, tags=["admin"], prefix="/admin")
api_router.include_router(head.router, tags=["head"], prefix="/head")
api_router.include_router(user.router, tags=["user"], prefix="/user")
api_router.include_router(engineer.router, tags=["engineer"], prefix="/engineer")
api_router.include_router(customer.router, tags=["customer"], prefix="/customer")
api_router.include_router(ticket.router, tags=["ticket"], prefix="/ticket")
api_router.include_router(ticket_allotment.router, tags=["allotment"], prefix="/ticket-allotment")
api_router.include_router(ticket_progress.router, tags=["progress"], prefix="/ticket-progress")
