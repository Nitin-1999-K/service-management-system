from fastapi import APIRouter

from .endpoints import admin, login, head

api_router = APIRouter()
api_router.include_router(admin.router, tags=["admin"], prefix="/admin")
api_router.include_router(head.router, tags=["head"], prefix="/head")
api_router.include_router(login.router, tags=["login"], prefix="/login")