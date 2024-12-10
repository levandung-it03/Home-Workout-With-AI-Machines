import math

import cv2
import numpy as np

from app.app_sql.setup_database import SessionLocal
from app.machine_cores import SiftBodyFat, ScheduleDecisionTree
from app.dtos.ScheduleDecisionDtos import DecideScheduleDto, NewScheduleDecisionDto, PaginatedScheduleDecisionDto
from app.app_sql.models import ScheduleDecision
from app.services.sql import ScheduleDecisionCrud
from app.services.sql.ScheduleDecisionCrud import page_size

global_schedule_decision_model = None

def schedule_decision_model_preparation_on_startup():
    global global_schedule_decision_model
    global_schedule_decision_model = ScheduleDecisionTree.trainScheduleDecide()


async def cal_body_fat_detection(image, gender):
    contents = await image.read()  # Read the file content
    img = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
    result = SiftBodyFat.siftDetection(img, gender)
    return dict([("bodyFatRatio", result)])


def decide_schedule_id(request: DecideScheduleDto):
    global global_schedule_decision_model
    result = ScheduleDecisionTree.predictScheduleId(request, global_schedule_decision_model)
    return {"scheduleId": int(result)}


def add_decision_schedule_dataline(request: NewScheduleDecisionDto):
    new_schedule = ScheduleDecision(
        age = request.age, gender = request.gender,
        weight = request.weight, body_fat_threshold = request.body_fat_threshold,
        session = request.session, schedule_id = request.schedule_id
    )
    db_session = SessionLocal()
    return ScheduleDecisionCrud.save(db_session, new_schedule).to_dict()


def delete_decision_schedule_dataline(line_id: int):
    db_session = SessionLocal()
    ScheduleDecisionCrud.deleteById(db_session, line_id)


def export_decision_schedule_dataset_to_csv():
    global global_schedule_decision_model
    db_session = SessionLocal()
    ScheduleDecisionCrud.export_to_csv(db_session)
    ScheduleDecisionTree.trainScheduleDecide(global_schedule_decision_model)


def get_schedule_decision_dataset_pages(request: PaginatedScheduleDecisionDto):
    db_session = SessionLocal()
    return {
        "data": [obj.to_dict() for obj in ScheduleDecisionCrud.findAllPaginated(db_session, request)],
        "currentPage": request.page,
        "totalPages": math.ceil(ScheduleDecisionCrud.countAll(db_session) / page_size),
    }
