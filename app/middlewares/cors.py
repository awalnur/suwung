from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class CustomCORSMiddleware(BaseHTTPMiddleware):
    """
    Custom middleware to handle CORS headers.
    if you need to customize the CORS headers, you can use this middleware.

    if you need to use the default CORS headers, you can use the starlette.middleware.cors.CORSMiddleware middleware.
    """
    def __init__(self, app, allow_origins=None, allow_methods=None, allow_headers=None, expose_headers=None, allow_credentials=True, max_age=600):
        super().__init__(app)
        self.allow_origins = allow_origins or ["*"]
        self.allow_methods = allow_methods or ["*"]
        self.allow_headers = allow_headers or ["*"]
        self.expose_headers = expose_headers or []
        self.allow_credentials = allow_credentials
        self.max_age = max_age

    async def dispatch(self, request, call_next):
        origin = request.headers.get("origin")

        # If origin is not allowed, don't set CORS headers
        if origin not in self.allow_origins and "*" not in self.allow_origins:
            return await call_next(request)

        # Handle OPTIONS (preflight) request
        if request.method == "OPTIONS":
            response = Response(status_code=204)  # No Content
            response.headers["Access-Control-Allow-Methods"] = ", ".join(self.allow_methods)
            response.headers["Access-Control-Allow-Headers"] = ", ".join(self.allow_headers)
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Max-Age"] = str(self.max_age)
            if self.allow_credentials:
                response.headers["Access-Control-Allow-Credentials"] = "true"
            return response

        # Handle actual request
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = ", ".join(self.allow_methods)
        response.headers["Access-Control-Allow-Headers"] = ", ".join(self.allow_headers)
        if self.expose_headers:
            response.headers["Access-Control-Expose-Headers"] = ", ".join(self.expose_headers)
        if self.allow_credentials:
            response.headers["Access-Control-Allow-Credentials"] = "true"
        return response