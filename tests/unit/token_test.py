import ast

import pytest
from pyseto import Token

from app.core.security import create_access_token, claim_access_token
test_env = {
    "SECRET_KEY": "test_secret"
}

def test_generate_token():
    data = {"sub": "test"}

    token = create_access_token(data)
    assert token is not None
    assert len(token) > 10

def test_generate_token_with_empty_data():
    data = {}

    token = create_access_token(data)
    assert token is not None
    assert len(token) > 10


def test_get_claim_token():
    data = {"sub": "test"}

    token  = create_access_token(data)

    claim = claim_access_token(token)
    assert claim is not None
    assert type(claim) == Token
    payload = ast.literal_eval(claim.payload.decode('utf-8'))
    assert payload == data


