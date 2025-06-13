"""
CRUD operations for Schedule
"""
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import date, datetime

from app.db.models.schedule import Schedule, ScheduleType
from app.db.schemas.schedule_schema import ScheduleCreate, ScheduleUpdate


def create_schedule(db: Session, schedule_in: ScheduleCreate) -> Schedule:
    """Create new schedule"""
    db_schedule = Schedule(**schedule_in.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


def get_schedule(db: Session, schedule_id: int) -> Optional[Schedule]:
    """Get schedule by ID with related media/playlist"""
    return db.query(Schedule)\
        .options(selectinload(Schedule.media), selectinload(Schedule.playlist))\
        .filter(Schedule.id == schedule_id).first()


def list_schedules(db: Session, skip: int = 0, limit: int = 100) -> List[Schedule]:
    """List schedules with pagination and related entities"""
    return db.query(Schedule)\
        .options(selectinload(Schedule.media), selectinload(Schedule.playlist))\
        .offset(skip).limit(limit).all()


def get_schedules_by_media(db: Session, media_id: int) -> List[Schedule]:
    """Get all schedules for a specific media"""
    return db.query(Schedule).filter(Schedule.media_id == media_id).all()


def get_schedules_by_playlist(db: Session, playlist_id: int) -> List[Schedule]:
    """Get all schedules for a specific playlist"""
    return db.query(Schedule).filter(Schedule.playlist_id == playlist_id).all()


def get_active_schedules(db: Session, schedule_type: Optional[str] = None) -> List[Schedule]:
    """Get all active schedules, optionally filtered by type"""
    query = db.query(Schedule)\
        .options(selectinload(Schedule.media), selectinload(Schedule.playlist))\
        .filter(Schedule.is_active == True)
    
    if schedule_type:
        query = query.filter(Schedule.schedule_type == schedule_type)
    
    return query.all()


def get_schedules_for_date(db: Session, target_date: date, weekday: int) -> List[Schedule]:
    """Get schedules that should run on a specific date and weekday"""
    schedules = []
    
    # Obtener schedules simples que incluyan este día de la semana
    simple_schedules = db.query(Schedule)\
        .options(selectinload(Schedule.media), selectinload(Schedule.playlist))\
        .filter(
            Schedule.is_active == True,
            Schedule.schedule_type == ScheduleType.simple
        ).all()
    
    for schedule in simple_schedules:
        if schedule.weekdays and weekday in schedule.weekdays:
            schedules.append(schedule)
    
    # Obtener schedules avanzados para esta fecha
    advanced_schedules = db.query(Schedule)\
        .options(selectinload(Schedule.media), selectinload(Schedule.playlist))\
        .filter(
            Schedule.is_active == True,
            Schedule.schedule_type == ScheduleType.advanced,
            or_(
                and_(
                    Schedule.start_date <= target_date,
                    Schedule.end_date >= target_date
                ),
                Schedule.specific_times.contains(str(target_date))
            )
        ).all()
    
    schedules.extend(advanced_schedules)
    
    # Ordenar por prioridad (mayor prioridad primero)
    return sorted(schedules, key=lambda x: x.priority, reverse=True)


def get_schedules_by_date_range(db: Session, start_date: date, end_date: date) -> List[Schedule]:
    """Get schedules that should run within a date range"""
    return db.query(Schedule)\
        .options(selectinload(Schedule.media), selectinload(Schedule.playlist))\
        .filter(
            Schedule.is_active == True,
            Schedule.schedule_type == ScheduleType.advanced,
            or_(
                and_(
                    Schedule.start_date <= end_date,
                    Schedule.end_date >= start_date
                ),
                # Para specific_times necesitaríamos una lógica más compleja
            )
        ).all()


def reorder_playlist_schedules(db: Session, playlist_id: int, schedule_orders: List[tuple]) -> bool:
    """Reorder schedules in a playlist. schedule_orders is a list of (schedule_id, new_order_index) tuples"""
    try:
        for schedule_id, new_order in schedule_orders:
            db.query(Schedule).filter(
                and_(Schedule.id == schedule_id, Schedule.playlist_id == playlist_id)
            ).update({"order_index": new_order})
        db.commit()
        return True
    except Exception:
        db.rollback()
        return False


def toggle_schedule_status(db: Session, schedule_id: int) -> Optional[Schedule]:
    """Toggle schedule active status"""
    schedule = get_schedule(db, schedule_id)
    if not schedule:
        return None
    
    schedule.is_active = not schedule.is_active
    db.commit()
    db.refresh(schedule)
    return schedule


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
