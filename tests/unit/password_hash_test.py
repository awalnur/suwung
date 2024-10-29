from app.security.password import PasswordHandler

handler = PasswordHandler

def test_generate_password_hash():
    password = "password"
    password_hash = handler.generate_password_hash(password)
    assert password_hash is not None
    assert len(password_hash) > 10
    assert password_hash != password

def test_verify_password():
    password = "password"
    password_hash = handler.generate_password_hash(password)

    assert handler.verify_password(password, password_hash)
    assert handler.verify_password("wrong_password", password_hash) != True
    assert handler.verify_password(password, handler.generate_password_hash("password2")) == False
    assert handler.verify_password("wrong_password", handler.generate_password_hash("password2")) == False