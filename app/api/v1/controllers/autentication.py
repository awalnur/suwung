from typing import Annotated

from fastapi import APIRouter, Depends, Header,HTTPException
from sqlalchemy.orm import Session

from app.api.v1.responses.authentication import Token
from app.db.session import get_db
from app.api.v1.requests.authentication import RequestAuthentication
from app.services.authentication import Authentication

router = APIRouter(prefix='/auth', tags=["Authentication"])


@router.post('/token', responses={200: {"description": "Get the authentication token",
                                        "model": Token}})
async def get_authentication_token(db: Annotated[Session, Depends(get_db)], payload: RequestAuthentication, X_Refresh_Token: str | None = Header(None, convert_underscores=True, title="X-Refresh-Token")):

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
    user_data = service.get_authentication(username=payload.username, password=payload.password)
    if user_data is None:
        raise HTTPException(401, "Invalid credentials")
    x_refresh_token = X_Refresh_Token
    if payload.grant_type =="refresh_token":
        if x_refresh_token is None:
            raise HTTPException(422, "Refresh token is required")

    response = Token(
        access_token="access_token",
        expires_in=3600,
        refresh_token="refresh"
    )
    return response

@router.get('/otp')
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