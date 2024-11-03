from sqlalchemy import Integer, Column

from app.app_sql.setup_database import Base, engine


class ScheduleDecision(Base):
    __tablename__ = "schedule_decision_dataset"

    id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer)
    gender = Column(Integer) # MALE(1), FEMALE(0)
    weight = Column(Integer)
    body_fat_threshold = Column(Integer)
    session = Column(Integer)
    schedule_id = Column(Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "age": self.age,
            "gender": self.gender,
            "weight": self.weight,
            "body_fat_threshold": self.body_fat_threshold,
            "session": self.session,
            "schedule_id": self.schedule_id,
        }


Base.metadata.create_all(engine)