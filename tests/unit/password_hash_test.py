import pytest
from app.core.password import generate_password_hash, verify_password


def test_generate_password_hash():
    password = "password"
    password_hash = generate_password_hash(password)
    assert password_hash is not None
    assert len(password_hash) > 10
    assert password_hash != password

def test_verify_password():
    password = "password"
    password_hash = generate_password_hash(password)

    assert verify_password(password, password_hash)
    assert verify_password("wrong_password", password_hash) != True
    assert verify_password(password, generate_password_hash("password2")) == False
    assert verify_password("wrong_password", generate_password_hash("password2")) == False