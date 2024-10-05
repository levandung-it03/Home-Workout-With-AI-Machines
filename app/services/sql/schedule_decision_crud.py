from sqlalchemy.orm import Session

from app.models import models
import pandas as pd
import os

def save(db: Session, scheduleDec: models.ScheduleDecision):
    db.add(scheduleDec)
    db.commit()
    db.refresh(scheduleDec)
    return scheduleDec

def findById(db: Session, decisionId: int):
    return db.query(models.ScheduleDecision).filter(models.ScheduleDecision.id == decisionId).first()

def deleteById(db: Session, decisionId: int):
    db.delete(findById(db, decisionId))
    db.commit()

def updateById(db: Session, decisionId: int, scheduleDec: models.ScheduleDecision):
    raw = db.query(models.ScheduleDecision).filter(models.ScheduleDecision.id == decisionId).first()
    if raw is None:
        return None
    raw.age = scheduleDec.age
    raw.gender = scheduleDec.gender
    raw.aim = scheduleDec.aim
    raw.weight = scheduleDec.weight
    raw.fat_ratio_range = scheduleDec.fat_ratio_range
    raw.schedule_id = scheduleDec.schedule_id
    db.commit()
    db.refresh(scheduleDec)
    return scheduleDec

def findAll(db: Session):
    return db.query(models.ScheduleDecision).all()

def findAllByScheduleId(db: Session, scheduleId: int):
    return db.query(models.ScheduleDecision).filter(models.ScheduleDecision.schedule_id == scheduleId).all()

def saveAll(db: Session, scheduleDecs: list[models.ScheduleDecision]):
    for schedule in scheduleDecs:
        db.add(schedule)
    db.commit()
    db.refresh(scheduleDecs)
    return scheduleDecs

def export_to_csv(db: Session):
    # d: all data for schedule decision
    d = db.query(models.ScheduleDecision).all()
    # f: convert all data (d) to Data Frame
    f = pd.DataFrame(ds.__dict__ for ds in d)
    # Drop the SQLAlchemy internal attributes
    f.drop(columns=['_sa_instance_state'], inplace=True)
    f.to_csv(os.path.join(os.getcwd(), 'dataset/ScheduleDecision.csv'), index=False)