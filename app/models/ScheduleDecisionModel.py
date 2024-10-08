from pydantic import BaseModel
from sqlalchemy import Column, Integer

from app.app_sql.database import Base


class ScheduleDecision(Base):
    __tablename__ = "schedule_decision_dataset"

    id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer)
    gender = Column(Integer) # MALE(1), FEMALE(0)
    aim = Column(Integer)    # WEIGHT_UP(1), MAINTAIN_WEIGHT(0), WEIGHT_DOWN(-1),
    weight = Column(Integer)
    min_fat_ratio = Column(Integer)
    max_fat_ratio = Column(Integer)
    schedule_id = Column(Integer)

class DecideScheduleDto(BaseModel):
    age: int
    gender: int # MALE(1), FEMALE(0)
    aim: int    # WEIGHT_UP(1), MAINTAIN_WEIGHT(0), WEIGHT_DOWN(-1),
    weight: int
    bodyFat: float