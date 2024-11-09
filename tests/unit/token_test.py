import ast

from pyseto import Token

from app.security.security import Security
test_env = {
    "SECRET_KEY": "very_secret"
}

def test_generate_token():
    data = {"sub": "test"}

    token = Security.generate_token(data)
    print(token)
    assert token is not None
    assert len(token) > 10

def test_generate_token_with_empty_data():
    data = {}

    token = Security.generate_token(data)
    assert token is not None
    assert len(token) > 10


def test_get_claim_token():
    data = {"sub": "test"}

    token  = Security.generate_token(data)
    print(token)
    claim = Security(token=token).claim_access_token()
    print(claim)
    assert claim is not None
    assert type(claim) == Token
    payload = ast.literal_eval(claim.payload.decode('utf-8'))
    print(payload)
    assert payload == data


