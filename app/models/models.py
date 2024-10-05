from sqlalchemy import Column, Integer, String

from app.app_sql.database import Base


class ScheduleDecision(Base):
    __tablename__ = "schedule_decision_dataset"

    id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer)
    gender = Column(Integer) # MALE(1), FEMALE(0)
    aim = Column(Integer)    # WEIGHT_UP(1), MAINTAIN_WEIGHT(0), WEIGHT_DOWN(-1),
    weight = Column(Integer)
    fat_ratio_range = Column(String)    # desc: 5_15, 15_25, 25_30, 30_100
    schedule_id = Column(Integer)