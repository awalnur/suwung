# api/error/exceptions.py
from typing import Any, Dict, Optional
from fastapi import HTTPException

class APIError(HTTPException):
    """Base API error class."""
    def __init__(
        self,
        status_code: int,
        message: str,
        error_code: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=message)
        self.error_code = error_code
        self.details = details or {}

class ValidationError(APIError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=400,
            message=message,
            error_code="VALIDATION_ERROR",
            details=details
        )

class AuthenticationError(APIError):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            status_code=401,
            message=message,
            error_code="AUTHENTICATION_ERROR"
        )

class AuthorizationError(APIError):
    def __init__(self, message: str = "Authorization Error"):
        super().__init__(
            status_code=403,
            message=message,
            error_code="AUTHORIZATION_ERROR"
        )

class NotFoundError(APIError):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            status_code=404,
            message=message,
            error_code="NOT_FOUND_ERROR"
        )

class ConflictError(APIError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=409,
            message=message,
            error_code="CONFLICT_ERROR",
            details=details
        )

class InternalServerError(APIError):
    def __init__(self, message: str = "Internal server error"):
        super().__init__(
            status_code=500,
            message=message,
            error_code="INTERNAL_SERVER_ERROR"
        )
