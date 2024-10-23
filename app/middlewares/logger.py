import time
import uuid
from fastapi import Request, FastAPI

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app.core.constants import COLORS
from app.core.logger import LoguruLogger, request_id_ctx_var


class RequestContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add request id to the context
    """

    def __init__(self,
         app: FastAPI,
         logger_instance: LoguruLogger,
        ):
        super().__init__(app)
        self.logger = logger_instance.get_logger()

        # Dynamic background color based on log level

    @staticmethod
    def _req_method_color(request_method):
        """ Return color based on log level """
        colors = {
            'GET': COLORS['BLUE_BG'],
            'HEAD': COLORS['WHITE_BG'],
            'POST': COLORS['GREEN_BG'],
            'PUT': COLORS['YELLOW_BG'],
            'DELETE': COLORS['RED_BG'],
            'PATCH': COLORS['CYAN_BG']
        }
        return colors.get(request_method, COLORS['WHITE_BG'])

    @staticmethod
    def _response_status_color(status_code):
        if 200 <= status_code < 300:
            return "<green>","</green>"
        elif 300 <= status_code < 400:
            return "<blue>", "</blue>"
        elif 400 <= status_code < 500:
            return "<yellow>", "</yellow>"
        else:
            return "<red>", "</red>"

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = str(uuid.uuid4())
        request_id_ctx_var.set(request_id)

        start_time = time.time()

        # TODO : Add request logging here if needed
        # self.logger.opt(colors=True).info(
        #     f"{self._method_color(request.method)} {request.method.ljust(8)}  {COLORS['RESET']} Request started for {request.url.path}",
        #     request_method=request.method,
        #     request_url=request.url.path,
        #     request_headers=request.headers,
        #     request_params=str(request.query_params),
        # )

        try:
            """ Process the request 
                Add more details to the log if needed, like request headers, query params etc.
            """
            response = await call_next(request)
            status_code = response.status_code
            color = self._response_status_color(status_code)
            process_time = (time.time()-start_time)*1000
            self.logger.opt(colors=True).info(
                f"{self._req_method_color(request.method)} {request.method.ljust(8)}  {COLORS['RESET']}"
                f"<cyan> {request.url.path}</cyan> "
                f"{color[0]}{status_code}{color[1]} - <yellow>{process_time:.2f}ms</yellow>",
                request_method=request.method,
                request_url=request.url.path,
                response_status=status_code,
                access_time_ms = process_time
            )
            return response

        except Exception as e:
            self.logger.error(
                f"Request failed {request.method} {request.url.path}",
                request_method=request.method,
                request_path=request.url.path,
                error=str(e)
            )
            raise

        finally:
            request_id_ctx_var.set("")



