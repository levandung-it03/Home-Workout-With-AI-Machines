import time
from typing import Dict, Any

from jose import JWTError, jwt
from starlette.config import environ

from app.api_helpers.CustomeExc import ApplicationException
from app.api_helpers.ErrorCodes import ErrorCodes

secret = environ.get("SECRET_KEY")


def verify_token_or_else_throw(token: str, is_ignore_expiry: bool) -> Dict[str, Any]:
    plain_token = token.split("Bearer ")[1] if ("Bearer " in token) else token
    try:
        parsed_claim = jwt.get_unverified_claims(plain_token)
        if parsed_claim["exp"] <= time.time():
            if not is_ignore_expiry:
                raise ApplicationException(ErrorCodes.EXPIRED_TOKEN)
        return parsed_claim
    except JWTError:
        raise ApplicationException(ErrorCodes.INVALID_TOKEN)