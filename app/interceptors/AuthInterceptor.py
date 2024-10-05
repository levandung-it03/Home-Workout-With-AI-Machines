import os

from dotenv import load_dotenv
from fastapi import Request, Response, FastAPI

from app.api_helpers.CustomeExc import ApplicationException
from app.api_helpers.ErrorCodes import ErrorCodes
from app.services.auth import Jwt
from app.services.redis.InvalidToken import InvalidToken

load_dotenv()

admin_endpoints = str(os.getenv("FAST_API_ADMIN_ENDPOINTS"))
user_endpoints = str(os.getenv("FAST_API_USER_ENDPOINTS"))

class AuthInterceptor:
    def __init__(self, app: FastAPI):
        self.app = app

    def turn_on(self):
        @self.app.middleware('http')
        async def dispatch(request: Request, call_next):
            if user_endpoints in request.url.path or admin_endpoints in request.url.path:
                # may throw ApplicationException (catch by ExcHandlers)
                parsed_claims = Jwt.verify_token_or_else_throw(request.headers["Authorization"], True)

                # check if accessToken is in blacklist
                invalid_token = InvalidToken(id=parsed_claims["jti"], expiryDate=parsed_claims["exp"])
                if invalid_token.find() is not None:
                    raise ApplicationException(ErrorCodes.LOGIN_SESSION_EXPIRED)

            # Call the next middleware or actual request handler
            response: Response = await call_next(request)

            return response