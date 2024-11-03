from typing import Optional

from pydantic import BaseModel, ConfigDict

class DecideScheduleDto(BaseModel):
    age: int
    gender: int # MALE(1), FEMALE(0)
    weight: int
    bodyFat: float
    session: int


class NewScheduleDecisionDto(BaseModel):
    age: int
    gender: int
    weight: int
    body_fat_threshold: float
    session: int
    schedule_id: int

class DeleteScheduleDecisionDto(BaseModel):
    dataline_id: int

class ScheduleDecisionDto(BaseModel):
    age: Optional[int] = None
    gender: Optional[int] = None
    weight: Optional[int] = None
    bodyFatThreshold: Optional[int] = None
    session: Optional[int] = None
    scheduleId: Optional[int] = None

class PaginatedScheduleDecisionDto(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    page: int
    sortedField: Optional[str] = None
    sortedMode: Optional[int] = None
    filterFields: Optional[ScheduleDecisionDto] = None