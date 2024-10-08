import cv2
import numpy as np

from app.machine_cores import SiftBodyFat, ScheduleDecisionTree
from app.models.ScheduleDecisionModel import DecideScheduleDto


async def cal_body_fat_detection(image, gender):
    contents = await image.read()  # Read the file content
    img = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
    result = SiftBodyFat.siftDetection(img, gender)
    return dict([("bodyFatRatio", result)])


def decide_schedule_id(request: DecideScheduleDto):
    result = ScheduleDecisionTree.scheduleDecide(request)
    return dict([("scheduleId", result)])