from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.security.security import oauth
from app.db.session import get_db
from app.api.v1.requests.authentication import RequestAuthentication
from app.services.authentication import Authentication

router = APIRouter(prefix='/auth', tags=["Authentication"], dependencies=[Depends(oauth)])


@router.post('/authentication')
async def get_authentication(db: Annotated[Session, Depends(get_db)], payload: RequestAuthentication):
    service = Authentication(db=db)
    """
    Check the health of the service.
    :return: x
    """
    # return service.get_authentication()
    return {'status': 'ok'}

@router.post('/request-otp')
async def get_request_otp():
    """
    Check the health of the service.
    :return: x
    """
    return {'status': 'ok'}

@router.post('/validate-otp')
async def get_validate_otp():
    """
    Check the health of the service.
    :return: x
    """
    return {'status': 'ok'}