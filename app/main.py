from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from memory_profiler import profile

from app.api import init_routers
from app.core.exceptions.handlers import init_exception_handler
from app.core.logger import hijack_uvicorn_logger
from app.core.telemetry import init_telemetry
from app.middlewares import setup_middlewares


def custom_openapi():
    """
    Generate a custom OpenAPI schema for the FastAPI application.

    Generate a custom OpenAPI schema for the FastAPI application.

    This function customizes the OpenAPI schema by adding a title, version,
    description, and a logo. It checks if the schema is already generated
    This function checks if the OpenAPI schema is already generated and cached.
    and returns it if available, otherwise, it creates a new schema.

    :return: The custom OpenAPI schema.
    """

    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API SUWUNG",
        version="0.1.0-dev",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema



@profile
def create_app()->FastAPI:
    """
    Create and configure an instance of the FastAPI application.

    This function sets up the FastAPI application by initializing routers,
    middlewares, and a custom logger.

    :return: An instance of the FastAPI application.
    """
    _app = FastAPI()

    # set custom openapi schema
    init_telemetry(_app)
    init_exception_handler(_app)
    # use custom logger
    hijack_uvicorn_logger()

    # init routers and middlewares
    init_routers(_app)
    setup_middlewares(_app)

    return _app

app = create_app()


app.openapi = custom_openapi
