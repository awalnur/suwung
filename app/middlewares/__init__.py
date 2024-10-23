from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.logger import logger_instance
from .logger import RequestContextMiddleware




def setup_middlewares(app: FastAPI):
    """
    this method is used to add middlewares to the FastAPI app.

    :param app:
    :return:
    """
    # If you want to add more middlewares, you can add them here

    # If you want to customize the CORS headers, you can use the CustomCORSMiddleware middleware.
    # If you need to use the default CORS headers, you can use the starlette.middleware.cors.CORSMiddleware middleware. the Cors middleware is already added by default.
    app.add_middleware(
                    CORSMiddleware,
                    allow_origins=["*"],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"]
    )

    # Adding the RequestContextMiddleware to the app

    app.add_middleware(RequestContextMiddleware, logger_instance=logger_instance)
