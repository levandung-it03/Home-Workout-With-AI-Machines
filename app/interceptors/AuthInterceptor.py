import os

from dotenv import load_dotenv
from fastapi import Request, Response, FastAPI

from app.services.auth import Jwt

load_dotenv()

admin_endpoints = str(os.getenv("FAST_API_ADMIN_ENDPOINTS"))
user_endpoints = str(os.getenv("FAST_API_USER_ENDPOINTS"))

class AuthInterceptor:
    def __init__(self, app: FastAPI):
        self.app = app

    def turn_on(self):
        @self.app.middleware('http')
        async def dispatch(request: Request, call_next):
            if user_endpoints in request.url or admin_endpoints in request.url:
                # may throw ApplicationException (catch by ExcHandlers)
                Jwt.verify_token_or_else_throw(request.headers["Authorization"], True)

            # Call the next middleware or actual request handler
            response: Response = await call_next(request)

            return response