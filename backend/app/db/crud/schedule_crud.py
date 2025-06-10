"""
CRUD operations for Schedule
"""
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.models.schedule import Schedule
from app.db.schemas.schedule_schema import ScheduleCreate, ScheduleUpdate


def create_schedule(db: Session, schedule_in: ScheduleCreate) -> Schedule:
    """Create new schedule"""
    db_schedule = Schedule(**schedule_in.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


def get_schedule(db: Session, schedule_id: int) -> Optional[Schedule]:
    """Get schedule by ID"""
    return db.query(Schedule).filter(Schedule.id == schedule_id).first()


def list_schedules(db: Session, skip: int = 0, limit: int = 100) -> List[Schedule]:
    """List schedules with pagination"""
    return db.query(Schedule).offset(skip).limit(limit).all()


def get_schedules_by_media(db: Session, media_id: int) -> List[Schedule]:
    """Get all schedules for a specific media"""
    return db.query(Schedule).filter(Schedule.media_id == media_id).all()


def update_schedule(db: Session, schedule_id: int, schedule_update: ScheduleUpdate) -> Optional[Schedule]:
    """Update schedule record"""
    db_schedule = get_schedule(db, schedule_id)
    if not db_schedule:
        return None
    
    update_data = schedule_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_schedule, field, value)
    
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


def delete_schedule(db: Session, schedule_id: int) -> bool:
    """Delete schedule record"""
    db_schedule = get_schedule(db, schedule_id)
    if not db_schedule:
        return False
    
    db.delete(db_schedule)
    db.commit()
    return True
