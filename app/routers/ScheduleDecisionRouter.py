import os

from dotenv import load_dotenv
from fastapi.params import Depends

from app.api_helpers.ApiResponse import ApiResponse
from app.api_helpers.SucceedCodes import SucceedCodes
from app.dtos.ScheduleDecisionDtos import DecideScheduleDto, NewScheduleDecisionDto, PaginatedScheduleDecisionDto, \
    DeleteScheduleDecisionDto
from app.services.business import ScheduleDecisionService
from fastapi import APIRouter, UploadFile, File, Form

load_dotenv()
admin_endpoints = str(os.getenv("FAST_API_ADMIN_ENDPOINTS"))
user_endpoints = str(os.getenv("FAST_API_USER_ENDPOINTS"))
router = APIRouter()

@router.post(admin_endpoints + "/v1/add-decision-schedule-dataline")
async def add_decision_schedule_dataline(request: NewScheduleDecisionDto):
    return ApiResponse(
        SucceedCodes.ADD_SCHEDULE_DATALINE,
        ScheduleDecisionService.add_decision_schedule_dataline(request))

@router.delete(admin_endpoints + "/v1/delete-decision-schedule-dataline")
async def add_decision_schedule_dataline(request: DeleteScheduleDecisionDto):
    ScheduleDecisionService.delete_decision_schedule_dataline(request.dataline_id)
    return ApiResponse(SucceedCodes.DELETE_SCHEDULE_DATALINE, None)

@router.put(admin_endpoints + "/v1/export-decision-schedule-dataset-to-csv")
async def export_decision_schedule_dataset_to_csv():
    ScheduleDecisionService.export_decision_schedule_dataset_to_csv()
    return ApiResponse(SucceedCodes.EXPORT_SCHEDULE_CSV, None)

@router.post(user_endpoints + "/v1/cal-body-fat-detection")
async def cal_body_fat_detection(image: UploadFile = File(...), gender: int = Form(...)):
    return ApiResponse(
        SucceedCodes.CAL_BODY_FAT,
        await ScheduleDecisionService.cal_body_fat_detection(image, gender))

@router.post(user_endpoints + "/v1/decide-schedule-id")
async def decide_schedule_id(request: DecideScheduleDto):
    return ApiResponse(
        SucceedCodes.SCHEDULE_DECISION,
        ScheduleDecisionService.decide_schedule_id(request))

@router.get(admin_endpoints + "/v1/get-schedule-decision-dataset-pages")
async def get_schedule_decision_dataset_pages(request: PaginatedScheduleDecisionDto = Depends()):
    return ApiResponse(
        SucceedCodes.GET_SCHEDULE_DATASET_PAGES,
        ScheduleDecisionService.get_schedule_decision_dataset_pages(request))