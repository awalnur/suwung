import random
from datetime import timedelta, datetime
from os import access

import requests
from memory_profiler import profile

from sqlalchemy.orm import Session

from app.core.logger import _logger as logger
from app.api.v1.requests.authentication import RequestAuthentication
from app.api.v1.responses.authentication import Token
from app.core.config import settings
from app.core.exceptions.exceptions import ValidationError, AuthorizationError, AuthenticationError
from app.db.repository.user import UserRepository
from app.security.password import PasswordHandler
from app.security.security import Security
from app.services.messaging import MessagingService


class Authentication:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository()
        self.messaging = MessagingService()

    def generate_refresh_token(self):

        token = Security.generate_random_code()
        return token


    async def basic_auth(self, username: str, password: str)->[str|None, str|None]:
        _userdata = self.repository.find_by_username(username=username)

        if _userdata is None:
            raise AuthenticationError

        hashed_password = next(iter(_userdata.password)).password_hash

        validate_password = PasswordHandler.verify_password(password, hashed_password)
        if not validate_password:
            raise AuthenticationError(message='invalid username or password')


        if _userdata.two_factor:
            print(_userdata.phone_number)
            otp = self.request_otp(to_phone_number=_userdata.phone_number, user_id=_userdata.id)
        payload = {'sub':str(_userdata.id), 'iat':datetime.now().timetuple()}

        try:
            access_token = Security.generate_token(data=payload, exp=settings.ACCESS_TOKEN_EXPIRATION, footer='access_token')
            refresh_token = Security.generate_token(data=payload,exp=settings.REFRESH_TOKEN_EXPIRATION, footer='refresh_token')
        except Exception as e:
            print(e)
            raise AuthenticationError(message='Error generating access token')

        await self.repository.set_refresh_token(_userdata, refresh_token)

        return access_token, refresh_token

    def token(self):
        pass

    def cred_with_refresh_token(self, refresh_token: str)->str|None:
        data = Security.claim_access_token(refresh_token)
        if data is None:
            raise AuthorizationError
        payload = {'sub':data['sub']}
        generate_token = Security.generate_token(data=payload)
        return generate_token

    async def get_authentication(self, payload: RequestAuthentication)->Token:

        _access_token, _refresh_token = None, None

        if payload.grant_type is None:
            raise ValidationError(message='Missing field required')

        _access_token, _refresh_token = await self.basic_auth(payload.username, payload.password)

        if _access_token is None:
            raise AuthenticationError

        response = Token(access_token=_access_token,
                         token_type='Bearer',
                         expires=3600,
                         refresh_token=_refresh_token)

        # user_data = self.repository.find_by_username(username=username)
        # return user_data

        return response

    # TODO : Implement this method
    #       - This method should be able to send OTP to a phone number
    #       - The phone number should be in the format of 62xxxxxxxxxx
    #     + Create TEST for this method
    def request_otp(self, to_phone_number: str, user_id: str):

        """
        Request OTP to a WhatsApp number

        Args:
            to_phone_number (str): Recipient's phone number with country code

        Returns:
            Dict: API response
        """
        try:
            logger.info(f"Requesting OTP to {to_phone_number}")

            if to_phone_number.startswith('+'):
                to_phone_number = to_phone_number[1:]

            verification_code = ''.join(random.choices('0123456789', k=6))
            template_components = {"components":[
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": verification_code
                        }
                    ]
                },
                {
                    "type": "button",
                    "sub_type": "url",
                    "index": 0,
                    "parameters": [
                        {
                            "type": "text",
                            "text": "Yes",
                            "payload": "yes"
                        }
                    ]
                }
            ]}

            _resp = self.messaging.send_template_message(
                to_phone_number=to_phone_number,
                template_name="hexalabauth",
                language_code="en",
                template_components=template_components
            )
                # if _resp.status_code == 200:
                #     print(f"OTP sent to {to_phone_number}")
                # print(_resp)
            if _resp.get("error"):
                logger.error(f"Failed to request OTP: {_resp}")
                raise Exception(f"Failed to request OTP: {_resp}")
            return _resp
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                print("Token tidak valid atau expired")
                print(f"Facebook Error: {e.response.json()}")
            elif e.response.status_code == 404:
                print("Endpoint tidak ditemukan")
            else:
                print(f"HTTP Error: {str(e)}")

        except Exception as e:
            logger.error(f"Failed to request OTP: {str(e)}")
            raise Exception(f"Failed to request OTP: {str(e)}")
