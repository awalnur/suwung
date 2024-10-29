import re
from venv import logger

import argon2 # pip install argon2-cffi


class PasswordHandler:
    def __init__(self, password: str):
        self.valid = self._validate_password(password)

    @staticmethod
    def _validate_password(_password):
        """
        Validate the password based on the following rules:
        :return:
        """
        if len(_password) < 8:
            """ Password must be at least 8 characters """
            return False, "Password must be at least 8 characters"

        if len(_password) > 64:
            """ Password must be at most 64 characters """
            return False, "Password must be at most 64 characters"

        if not re.search(r"[A-Z]", _password):
            """ Password must contain at least one digit """
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r"[a-z]", _password):
            """ Password must contain at least one lowercase letter """
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r"[!@#$%^&*()]", _password):
            """ Password must contain at least one special character """
            return False, "Password must contain at least one special character"
        if re.search(r"\s", _password):
            """ Password must not contain any spaces """

            return False, "Password must not contain any spaces"

        if not re.search(r"\d", _password):
            """ Password must not be all digits """
            return False, "Password must contain at least one digit"
        return True, None

    def __repr__(self):
        return f"PasswordHandler(valid={self.valid})"


    @staticmethod
    def generate_password_hash(password: str) -> str:
        """

        Hash a password using Argon2.

        Args:
            password (str): The plain text password to hash.

        Returns:
            str: The Argon2 hash of the password.
        """
        return argon2.PasswordHasher(salt_len=16).hash(password)


    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verify a password against a hashed password.

        :arg
            password: The plain text password to verify.
            hashed_password: The hashed password to verify against.
        :returns:
            True if the password matches the hashed password, False otherwise.
        """
        try:
            argon2.PasswordHasher(salt_len=16).verify(password=password, hash=hashed_password)
            return True
        except argon2.exceptions.VerifyMismatchError:
            return False

