from fastapi import APIRouter, FastAPI

from .v1 import check, autentication

v1 = APIRouter(prefix='/v1')
v1.include_router(autentication.router, tags=["Authentication"])
v1.include_router(check.router)

# Compare this snippet from app/api/v1/check.py:

def init_routers(app: FastAPI):
    app.include_router(v1)