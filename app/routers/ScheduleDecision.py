import os

from dotenv import load_dotenv

from app.api_helpers.ApiResponse import ApiResponse
from app.api_helpers.SucceedCodes import SucceedCodes
from app.dtos.request import TestToken
from app.services.auth import Jwt
from app.services.bussiness import ScheduleDecision
from fastapi import APIRouter, UploadFile, File

load_dotenv()
admin_endpoints = str(os.getenv("FAST_API_ADMIN_ENDPOINTS"))
user_endpoints = str(os.getenv("FAST_API_USER_ENDPOINTS"))
router = APIRouter()

@router.post(user_endpoints + "/v1/cal-body-fat-detection")
async def cal_body_fat_detection(img: UploadFile = File(...)):
    return ApiResponse(SucceedCodes.CAL_BODY_FAT, ScheduleDecision.cal_body_fat_detection(img))

@router.post(admin_endpoints + "/test")
async def test(request: TestToken):
    return ApiResponse(SucceedCodes.AUTHENTICATION, dict([
        ("test", "succeed"),
        ("claims", Jwt.verify_token_or_else_throw(request.token, False))
    ]))