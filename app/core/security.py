import ast

import pyseto
from pyseto import Key, Token

from app.core.config import settings



def create_access_token(data: dict):
    paseto=Key.new(version=4, purpose='local', key=settings.SECRET_KEY)
    try:
        token = pyseto.encode(paseto, data)
        return token
    except pyseto.EncryptError as e:
        return e

def claim_access_token(access_token: str)->Token:
    paseto=Key.new(version=4, purpose='local', key=settings.SECRET_KEY)
    try:
        data = pyseto.decode(paseto, access_token)
        # payload = ast.literal_eval(data.decode('utf-8'))s

        return data
    except pyseto.DecryptError as e:
        _logger.error
        return e

