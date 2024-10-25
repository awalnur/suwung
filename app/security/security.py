
import pyseto
from fastapi.security import APIKeyHeader
from pyseto import Key, Token

from app.core.config import settings
from app.core.logger import _logger

oauth = APIKeyHeader(name='Authorization', scheme_name='authorization')

def create_access_token(data: dict):
    """
    Create an access token using PASETO (Platform-Agnostic Security Tokens).

    :param data: A dictionary containing the data to be encoded in the token.
    :return: The encoded access token as a string.
    """
    paseto=Key.new(version=4, purpose='local', key=settings.SECRET_KEY)
    try:
        token = pyseto.encode(paseto, data)
        return token
    except pyseto.EncryptError as e:
        _logger.error(f"Error decoding token: {e}")

        return e

def claim_access_token(access_token: str)->Token:
    paseto=Key.new(version=4, purpose='local', key=settings.SECRET_KEY)
    try:
        data = pyseto.decode(paseto, access_token)
        return data
    except pyseto.DecryptError as e:
        _logger.error(f"Error decoding token: {e}")
        return e

