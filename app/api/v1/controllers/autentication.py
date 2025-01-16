from typing import Annotated

from fastapi import APIRouter, Depends, Header,HTTPException,Security
from sqlalchemy.orm import Session

from app.api.v1.responses.authentication import Token
from app.db.session import get_db
from app.api.v1.requests.authentication import RequestAuthentication
from app.security.security import oauth, Security as Sec
from app.services.authentication import Authentication
from app.services.messaging import MessagingService

router = APIRouter(prefix='/auth', tags=["Authentication"])


# TODO : create endpoint
#   - auth/authentication its can use the token
#   - auth/otp [GET, POST]
#   - auth/otp [GET, POST]
#   - auth/refresh -> revoke and replace token with new token
#   - auth/revoke ->revoke all token
#   - auth/reset-password
#   - auth/change-password
#   - auth/me
#   - auth/scope


@router.post('/token', responses={200: {"description": "Get the authentication token",
                                        "model": Token}})
async def get_authentication_token(db: Annotated[Session, Depends(get_db)], payload: RequestAuthentication):
    """
    Endpoint to obtain an authentication token.

    Args:
        payload (RequestAuthentication): Request payload containing username, password, grant type, and scope.
        :param db: Database session dependency.
        :param payload: Request payload containing username, password, grant type, and scope.
        :param x_refresh_token:

    Returns:
        Token: Response model containing access token, token type, expiration time, and refresh token.
    """
    service = Authentication(db=db)
    response = await service.get_authentication(payload=payload)

    return response
@router.post('/refresh-token')
async def get_refresh_token(db: Annotated[Session, Depends(get_db)], X_Refresh_Token: str = Header(alias='X-Refresh-Token')):
    """
    Check the health of the service.
    :return: x
    """
    refresh = Authentication(db=db)
    response = await refresh.cred_with_refresh_token(refresh_token=X_Refresh_Token)
    return {'status': 'ok'}

@router.get('/otp')
async def get_request_otp(db: Annotated[Session, Depends(get_db)], phone_number: str):
    """
    Check the health of the service.
    :return: x
    """
    messaging = Authentication(db=db)
    messaging.request_otp(to_phone_number=phone_number)
    return {'status': 'ok'}

@router.post('/otp')
async def validate_otp():

    return {'status': 'ok'}

@router.post('/validate-otp')
async def get_validate_otp():
    """
    Check the health of the service.
    :return: x
    """
    return {'status': 'ok'}

@router.get('/me')
async def get_my_data(db: Annotated[Session, Depends(get_db)], token: Annotated[Security, Depends(Sec)]):
    return {'status': token}

