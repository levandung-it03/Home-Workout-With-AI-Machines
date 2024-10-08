import os

from dotenv import load_dotenv
from pydantic import BaseModel

from app.api_helpers.ApiResponse import ApiResponse
from app.api_helpers.SucceedCodes import SucceedCodes
from app.services.auth import Jwt
from fastapi import APIRouter

load_dotenv()
admin_endpoints = str(os.getenv("FAST_API_ADMIN_ENDPOINTS"))
user_endpoints = str(os.getenv("FAST_API_USER_ENDPOINTS"))
router = APIRouter()


class TestToken(BaseModel):
    token: str


@router.post("/api/private/admin/test")
async def test(request: TestToken):
    return ApiResponse(SucceedCodes.AUTHENTICATION, dict([
        ("test", "succeed"),
        ("claims", Jwt.verify_token_or_else_throw(request.token, False))
    ]))

@router.get("/test")
async def test2():
    return "s"