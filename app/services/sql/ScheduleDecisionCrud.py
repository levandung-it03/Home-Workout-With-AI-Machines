from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from app.app_sql.models import ScheduleDecision
import pandas as pd
import os

from app.dtos.ScheduleDecisionDtos import PaginatedScheduleDecisionDto

page_size = 30

def save(db: Session, scheduleDec: ScheduleDecision):
    db.add(scheduleDec)
    db.commit()
    db.refresh(scheduleDec)
    return scheduleDec

def findById(db: Session, decisionId: int):
    return db.query(ScheduleDecision).filter(ScheduleDecision.id == decisionId).first()

def deleteById(db: Session, decisionId: int):
    db.delete(findById(db, decisionId))
    db.commit()

def updateById(db: Session, decisionId: int, scheduleDec: ScheduleDecision):
    raw = db.query(ScheduleDecision).filter(ScheduleDecision.id == decisionId).first()
    if raw is None:
        return None
    raw.age = scheduleDec.age
    raw.gender = scheduleDec.gender
    raw.weight = scheduleDec.weight
    raw.body_fat_threshold = scheduleDec.body_fat_threshold
    raw.schedule_id = scheduleDec.schedule_id
    db.commit()
    db.refresh(scheduleDec)
    return scheduleDec

def findAll(db: Session):
    return db.query(ScheduleDecision).all()

def findAllPaginated(db: Session, request: PaginatedScheduleDecisionDto):
    query = db.query(ScheduleDecision)

    # Apply filtering based on the request
    if request.filterFields is not None:
        if request.filterFields.age is not None:
            query = query.filter(ScheduleDecision.age == request.filterFields.age)
        if request.filterFields.gender is not None:
            query = query.filter(ScheduleDecision.gender == request.filterFields.gender)
        if request.filterFields.weight is not None:
            query = query.filter(ScheduleDecision.weight == request.filterFields.weight)
        if request.filterFields.body_fat_threshold is not None:
            query = query.filter(ScheduleDecision.body_fat_threshold == request.filterFields.bodyFatThreshold)
        if request.filterFields.session is not None:
            query = query.filter(ScheduleDecision.session == request.filterFields.session)
        if request.filterFields.schedule_id is not None:
            query = query.filter(ScheduleDecision.schedule_id == request.filterFields.scheduleId)

    # Apply sorting
    if request.sortedField is not None and request.sortedMode in [1, -1]:
        sort_order = asc if request.sortedMode == 1 else desc
        query = query.order_by(sort_order(getattr(ScheduleDecision, request.sortedField)))

    # Pagination
    offset = (request.page - 1) * page_size
    results = query.offset(offset).limit(page_size).all()

    return results

def findAllByScheduleId(db: Session, scheduleId: int):
    return db.query(ScheduleDecision).filter(ScheduleDecision.schedule_id == scheduleId).all()

def saveAll(db: Session, scheduleDecs: list[ScheduleDecision]):
    for schedule in scheduleDecs:
        db.add(schedule)
    db.commit()
    db.refresh(scheduleDecs)
    return scheduleDecs

def countAll(db: Session):
    return db.query(ScheduleDecision).count()

def export_to_csv(db: Session):
    # d: all data for schedule decision
    d = (db.query(ScheduleDecision).order_by(
        ScheduleDecision.age, ScheduleDecision.schedule_id, ScheduleDecision.gender, ScheduleDecision.weight)
    .all())

    # f: convert all data (d) to Data Frame
    f = pd.DataFrame(ds.__dict__ for ds in d)

    # Drop the SQLAlchemy internal attributes and 'id' column data
    f.drop(columns=['_sa_instance_state', 'id'], inplace=True)
    f.to_csv(os.path.join(os.getcwd(), 'app/dataset/csv/schedule.csv'), index=False)