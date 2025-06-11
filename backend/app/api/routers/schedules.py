"""
Schedule router for content scheduling
"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.db.crud import schedule_crud
from app.db.schemas.schedule_schema import ScheduleCreate, ScheduleRead, ScheduleUpdate
from app.api.routers.auth import get_current_user
from app.db.models.user import User
from app.core.websocket_manager import broadcast_event

router = APIRouter()


@router.post("/", response_model=ScheduleRead)
def create_schedule(
    schedule: ScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Create new schedule"""
    new_schedule = schedule_crud.create_schedule(db=db, schedule_in=schedule)
    background_tasks.add_task(broadcast_event, "schedule_created", {"id": new_schedule.id})
    return new_schedule


@router.get("/", response_model=List[ScheduleRead])
def list_schedules(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all schedules"""
    return schedule_crud.list_schedules(db, skip=skip, limit=limit)


@router.get("/media/{media_id}", response_model=List[ScheduleRead])
def get_schedules_by_media(
    media_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all schedules for specific media"""
    return schedule_crud.get_schedules_by_media(db, media_id=media_id)


@router.get("/{schedule_id}", response_model=ScheduleRead)
def get_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific schedule by ID"""
    schedule = schedule_crud.get_schedule(db, schedule_id=schedule_id)
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )
    return schedule


@router.put("/{schedule_id}", response_model=ScheduleRead)
def update_schedule(
    schedule_id: int,
    schedule_update: ScheduleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Update schedule"""
    schedule = schedule_crud.update_schedule(
        db, schedule_id=schedule_id, schedule_update=schedule_update
    )
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )
    background_tasks.add_task(broadcast_event, "schedule_updated", {"id": schedule.id})
    return schedule


@router.delete("/{schedule_id}")
def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Delete schedule"""
    success = schedule_crud.delete_schedule(db, schedule_id=schedule_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )
    background_tasks.add_task(broadcast_event, "schedule_deleted", {"id": schedule_id})
    return {"message": "Schedule deleted successfully"}