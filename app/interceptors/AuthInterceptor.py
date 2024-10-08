import os

from dotenv import load_dotenv
from fastapi import Request, Response, FastAPI

from app.api_helpers.ApiResponse import ApiResponse
from app.api_helpers.CustomeExc import ApplicationException
from app.api_helpers.ErrorCodes import ErrorCodes
from app.app_redis.redis_con import RedisConnection
from app.services.auth import Jwt

load_dotenv()

admin_prefix = str(os.getenv("FAST_API_ADMIN_ENDPOINTS"))
user_prefix = str(os.getenv("FAST_API_USER_ENDPOINTS"))


class AuthInterceptor:
    def __init__(self, app: FastAPI):
        self.app = app

    def turn_on(self):
        @self.app.middleware('http')
        async def dispatch(request: Request, call_next):
            print(f"Request: {request.method} {request.url}")
            if request.method != "OPTIONS" and (user_prefix in request.url.path or admin_prefix in request.url.path):
                try:
                    token = request.headers["Authorization"]
                except KeyError:
                    raise ApplicationException(ErrorCodes.INVALID_TOKEN)

                parsed_claims = Jwt.verify_token_or_else_throw(token, False)

                # check if accessToken is in blacklist
                redis_jti = RedisConnection.hget(f'InvalidToken:{parsed_claims['jti']}', "id")
                if redis_jti == parsed_claims['jti']:
                    raise ApplicationException(ErrorCodes.LOGIN_SESSION_EXPIRED)

                # invalid role accessing
                if parsed_claims['scope'].split("ROLE_")[1] not in request.url.path.upper():
                    raise ApplicationException(ErrorCodes.INVALID_TOKEN)

            # Call the next middleware or actual request handler
            response: Response = await call_next(request)

            return response
