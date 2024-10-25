import pytest

from app.security.password import PasswordHandler


@pytest.mark.parametrize("password, expected", [
    ("Short1!", False),  # Too short
    ("ThisIsAVeryLongPasswordThatExceedsTheMaximumAllowedLength123asdasd!", False),  # Too long
    ("NoDigitsHere!", False),  # No digits
    ("nouppercase1!", False),  # No uppercase letters
    ("NOLOWERCASE1!", False),  # No lowercase letters
    ("NoSpecialChar1", False),  # No special characters
    ("ValidPassword1!@", True),  # Valid password
    ("Invalid Password1!", False),  # Contains spaces
    ("12345678!", False),  # All digits
])
def test_validate_password(password, expected):
    validate = PasswordHandler(password)
    assert validate.valid[0] == expected