import random
import string

import pyseto
from hashlib import sha256
from fastapi.params import Depends
from fastapi.security import APIKeyHeader
from pyseto import Key, Token

from app.core.config import settings
from app.core.exceptions.exceptions import AuthorizationError
from app.core.logger import _logger

oauth = APIKeyHeader(name='Authorization', scheme_name='authorization')


class Security:
    def __init__(self, token = Depends(oauth)):
        self.token = token if token is not None else oauth
        self._validate_oauth()

    def _validate_oauth(self):

        claim = self.claim_access_token()
        if claim is None:
            raise AuthorizationError

    def claim_access_token(self, access_token: str = None) -> Token | None:
        if access_token is None:
            access_token = self.token

        if type(access_token) is str:
            access_token = bytes(access_token, 'utf-8')

        paseto = Key.new(version=4, purpose='local', key=settings.SECRET_KEY)
        try:
            data = pyseto.decode(paseto, access_token)
        except pyseto.DecryptError as e:
            _logger.error(f"Error decoding token: {e}")
            data =  None
        except Exception as e:
            _logger.error(f'{e}')
            data = None

        return data


    @staticmethod
    def generate_token(data: dict, exp: int=settings.ACCESS_TOKEN_EXPIRATION, footer: str = 'access token') -> str:
        """
        Create an access token using PASETO (Platform-Agnostic Security Tokens).

        :param data: A dictionary containing the data to be encoded in the token.
        :return: The encoded access token as a string.
        """
        paseto=Key.new(version=4, purpose='local', key=settings.SECRET_KEY)
        try:
            token = pyseto.encode(paseto, data, exp=exp, footer=footer)
            return token
        except pyseto.EncryptError as e:
            _logger.error(f"Error encode token: {e}")

            return e

    @staticmethod
    def generate_random_code():
        """

        :return:
        """
        _code = ''.join(random.choice(string.ascii_letters + string.digits+string.punctuation) for _ in range(32))

        return _code



    #
    # def claim_access_token(access_token: str)->Token:
    #     paseto=Key.new(version=4, purpose='local', key=settings.SECRET_KEY)
    #     try:
    #         data = pyseto.decode(paseto, access_token)
    #         return data
    #     except pyseto.DecryptError as e:
    #         _logger.error(f"Error decoding token: {e}")
    #         return e

