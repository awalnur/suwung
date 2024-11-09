from pyexpat.errors import messages

import starlette.status
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

from app.core.exceptions.exceptions import ConflictError, APIError


def init_exception_handler(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        _error_data =exc.errors()[0]
        detail = _error_data['type'] +' required Field'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    @app.exception_handler(APIError)
    async def conflict_exception(req, exc: APIError):
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)

    @app.exception_handler(500)
    async def internal_exception(req, exc: Exception):
        return JSONResponse(status_code=500, content=jsonable_encoder({"detail": "Ups, Something was wrong"}))
