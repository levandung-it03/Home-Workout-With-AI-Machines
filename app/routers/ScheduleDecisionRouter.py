import os

from dotenv import load_dotenv

from app.api_helpers.ApiResponse import ApiResponse
from app.api_helpers.SucceedCodes import SucceedCodes
from app.models.Enums import Gender
from app.models.ScheduleDecisionModel import DecideScheduleDto
from app.services.business import ScheduleDecisionService
from fastapi import APIRouter, UploadFile, File

load_dotenv()
admin_endpoints = str(os.getenv("FAST_API_ADMIN_ENDPOINTS"))
user_endpoints = str(os.getenv("FAST_API_USER_ENDPOINTS"))
router = APIRouter()

@router.post(user_endpoints + "/v1/cal-body-fat-detection")
async def cal_body_fat_detection(image: UploadFile = File(...), gender: int = Gender.GENDER_MALE):
    return ApiResponse(SucceedCodes.CAL_BODY_FAT, await ScheduleDecisionService.cal_body_fat_detection(image, gender))

@router.post(admin_endpoints + "/v1/decide-schedule-id")
async def decide_schedule_id(request: DecideScheduleDto):
    return ApiResponse(SucceedCodes.SCHEDULE_DECISION, ScheduleDecisionService.decide_schedule_id(request))