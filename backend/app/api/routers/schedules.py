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


# =============================================================================
# PLAYLIST ENDPOINTS (Incluidos en schedules router para evitar problemas)
# =============================================================================

@router.get("/playlist-stats", tags=["playlists"])
def get_playlist_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get playlist statistics"""
    try:
        from app.db.crud import playlist_crud
        stats = playlist_crud.get_playlist_stats(db)
        
        return {
            "total_playlists": stats.total_playlists,
            "total_scheduled_items": stats.total_scheduled_items
        }
    except ImportError:
        return {"total_playlists": 0, "total_scheduled_items": 0}
    except Exception as e:
        print(f"Error getting playlist stats: {e}")
        return {"total_playlists": 0, "total_scheduled_items": 0}


@router.get("/playlist-list", tags=["playlists"])
def list_playlists(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all playlists"""
    try:
        from app.db.crud import playlist_crud
        playlists = playlist_crud.list_playlists(db, skip=skip, limit=limit)
        
        result = []
        for p in playlists:
            try:
                playlist_dict = {
                    "id": p.id,
                    "name": p.name or "",
                    "description": p.description or "",
                    "created_at": p.created_at.isoformat() if p.created_at else None,
                    "updated_at": p.updated_at.isoformat() if p.updated_at else None,
                }
                result.append(playlist_dict)
            except Exception as e:
                print(f"Error processing playlist {p.id}: {e}")
                continue
        
        return result
    except ImportError:
        return []
    except Exception as e:
        print(f"Error listing playlists: {e}")
        return []


@router.post("/playlist-create", tags=["playlists"])
def create_playlist(
    playlist_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Create new playlist"""
    try:
        from app.db.crud import playlist_crud
        from app.db.schemas.playlist_schema import PlaylistCreate
        
        # Validar nombre antes de crear el schema
        if not playlist_data.get("name", "").strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El nombre de la playlist no puede estar vacío"
            )
        
        playlist_in = PlaylistCreate(**playlist_data)
        new_playlist = playlist_crud.create_playlist(db=db, playlist_in=playlist_in)
        
        background_tasks.add_task(broadcast_event, "playlist_created", {"id": new_playlist.id})
        
        return {
            "id": new_playlist.id,
            "name": new_playlist.name,
            "description": new_playlist.description,
            "created_at": new_playlist.created_at.isoformat() if new_playlist.created_at else None,
            "updated_at": new_playlist.updated_at.isoformat() if new_playlist.updated_at else None,
        }
    except HTTPException:
        raise
    except ImportError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Playlist functionality not available"
        )
    except Exception as e:
        print(f"Error creating playlist: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating playlist"
        )


@router.get("/playlist-get/{playlist_id}", tags=["playlists"])
def get_playlist(
    playlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific playlist by ID"""
    try:
        from app.db.crud import playlist_crud
        
        playlist = playlist_crud.get_playlist(db, playlist_id=playlist_id)
        
        if not playlist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Playlist not found"
            )
        
        return {
            "id": playlist.id,
            "name": playlist.name,
            "description": playlist.description,
            "created_at": playlist.created_at.isoformat() if playlist.created_at else None,
            "updated_at": playlist.updated_at.isoformat() if playlist.updated_at else None,
        }
    except ImportError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Playlist functionality not available"
        )


@router.put("/playlist-update/{playlist_id}", tags=["playlists"])
def update_playlist(
    playlist_id: int,
    playlist_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Update playlist"""
    try:
        from app.db.crud import playlist_crud
        from app.db.schemas.playlist_schema import PlaylistUpdate
        
        playlist_update = PlaylistUpdate(**playlist_data)
        playlist = playlist_crud.update_playlist(
            db, playlist_id=playlist_id, playlist_update=playlist_update
        )
        
        if not playlist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Playlist not found"
            )
        
        background_tasks.add_task(broadcast_event, "playlist_updated", {"id": playlist.id})
        
        return {
            "id": playlist.id,
            "name": playlist.name,
            "description": playlist.description,
            "created_at": playlist.created_at.isoformat() if playlist.created_at else None,
            "updated_at": playlist.updated_at.isoformat() if playlist.updated_at else None,
        }
    except ImportError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Playlist functionality not available"
        )


@router.delete("/playlist-delete/{playlist_id}", tags=["playlists"])
def delete_playlist(
    playlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Delete playlist"""
    try:
        from app.db.crud import playlist_crud
        
        success = playlist_crud.delete_playlist(db, playlist_id=playlist_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Playlist not found"
            )
        
        background_tasks.add_task(broadcast_event, "playlist_deleted", {"id": playlist_id})
        return {"message": "Playlist deleted successfully"}
    except ImportError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Playlist functionality not available"
        )


# =============================================================================
# SCHEDULE ENDPOINTS
# =============================================================================

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


# =============================================================================
# ADVANCED SCHEDULING ENDPOINTS
# =============================================================================

@router.get("/schedules/active", tags=["advanced-scheduling"])
def get_active_schedules(
    schedule_type: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all active schedules, optionally filtered by type (simple/advanced)"""
    # Validar schedule_type si se proporciona
    if schedule_type and schedule_type not in ["simple", "advanced"]:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail="schedule_type must be 'simple' or 'advanced'")
    
    try:
        schedules = schedule_crud.get_active_schedules(db, schedule_type=schedule_type)
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Error fetching schedules: {str(e)}")
    
    result = []
    for schedule in schedules:
        schedule_data = {
            "id": schedule.id,
            "schedule_type": schedule.schedule_type,
            "is_active": schedule.is_active,
            "priority": schedule.priority,
            "created_at": schedule.created_at.isoformat() if schedule.created_at else None
        }
        
        # Datos específicos según el tipo de schedule
        if schedule.schedule_type == "simple":
            schedule_data.update({
                "is_all_day": schedule.is_all_day,
                "daily_start": schedule.daily_start,
                "daily_end": schedule.daily_end,
                "weekdays": schedule.weekdays
            })
        elif schedule.schedule_type == "advanced":
            schedule_data.update({
                "start_date": schedule.start_date.isoformat() if schedule.start_date else None,
                "end_date": schedule.end_date.isoformat() if schedule.end_date else None,
                "specific_times": schedule.specific_times
            })
        
        # Información del contenido programado
        if schedule.media:
            schedule_data["content"] = {
                "type": "media",
                "id": schedule.media.id,
                "filename": schedule.media.filename,
                "media_type": schedule.media.media_type,
                "duration": schedule.media.duration
            }
        elif schedule.playlist:
            schedule_data["content"] = {
                "type": "playlist",
                "id": schedule.playlist.id,
                "name": schedule.playlist.name,
                "description": schedule.playlist.description
            }
        
        result.append(schedule_data)
    
    return result


@router.get("/for-date/{target_date}", tags=["advanced-scheduling"])
def get_schedules_for_date(
    target_date: str,  # Format: YYYY-MM-DD
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get schedules that should run on a specific date"""
    try:
        from datetime import datetime
        
        # Parsear la fecha
        date_obj = datetime.strptime(target_date, "%Y-%m-%d").date()
        weekday = date_obj.weekday()  # 0=Monday, 6=Sunday
        
        schedules = schedule_crud.get_schedules_for_date(db, date_obj, weekday)
        
        result = []
        for schedule in schedules:
            schedule_data = {
                "id": schedule.id,
                "schedule_type": schedule.schedule_type,
                "priority": schedule.priority,
                "is_all_day": schedule.is_all_day,
                "daily_start": schedule.daily_start,
                "daily_end": schedule.daily_end
            }
            
            # Información del contenido
            if schedule.media:
                schedule_data["content"] = {
                    "type": "media",
                    "id": schedule.media.id,
                    "filename": schedule.media.filename,
                    "media_type": schedule.media.media_type,
                    "duration": schedule.media.duration
                }
            elif schedule.playlist:
                schedule_data["content"] = {
                    "type": "playlist",
                    "id": schedule.playlist.id,
                    "name": schedule.playlist.name
                }
            
            result.append(schedule_data)
        
        return result
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD"
        )


@router.get("/media/{media_id}", tags=["advanced-scheduling"])
def get_schedules_by_media(
    media_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all schedules for a specific media"""
    schedules = schedule_crud.get_schedules_by_media(db, media_id)
    
    result = []
    for schedule in schedules:
        schedule_data = {
            "id": schedule.id,
            "schedule_type": schedule.schedule_type,
            "is_active": schedule.is_active,
            "priority": schedule.priority,
            "created_at": schedule.created_at.isoformat() if schedule.created_at else None
        }
        
        if schedule.schedule_type == "simple":
            schedule_data.update({
                "is_all_day": schedule.is_all_day,
                "daily_start": schedule.daily_start,
                "daily_end": schedule.daily_end,
                "weekdays": schedule.weekdays
            })
        elif schedule.schedule_type == "advanced":
            schedule_data.update({
                "start_date": schedule.start_date.isoformat() if schedule.start_date else None,
                "end_date": schedule.end_date.isoformat() if schedule.end_date else None,
                "specific_times": schedule.specific_times
            })
        
        result.append(schedule_data)
    
    return result


@router.get("/playlist/{playlist_id}", tags=["advanced-scheduling"])
def get_schedules_by_playlist(
    playlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all schedules for a specific playlist"""
    schedules = schedule_crud.get_schedules_by_playlist(db, playlist_id)
    
    result = []
    for schedule in schedules:
        schedule_data = {
            "id": schedule.id,
            "schedule_type": schedule.schedule_type,
            "is_active": schedule.is_active,
            "priority": schedule.priority,
            "created_at": schedule.created_at.isoformat() if schedule.created_at else None
        }
        
        if schedule.schedule_type == "simple":
            schedule_data.update({
                "is_all_day": schedule.is_all_day,
                "daily_start": schedule.daily_start,
                "daily_end": schedule.daily_end,
                "weekdays": schedule.weekdays
            })
        elif schedule.schedule_type == "advanced":
            schedule_data.update({
                "start_date": schedule.start_date.isoformat() if schedule.start_date else None,
                "end_date": schedule.end_date.isoformat() if schedule.end_date else None,
                "specific_times": schedule.specific_times
            })
        
        result.append(schedule_data)
    
    return result


@router.patch("/{schedule_id}/toggle", tags=["advanced-scheduling"])
def toggle_schedule_status(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Toggle schedule active status"""
    schedule = schedule_crud.toggle_schedule_status(db, schedule_id)
    
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )
    
    background_tasks.add_task(broadcast_event, "schedule_toggled", {
        "id": schedule.id,
        "is_active": schedule.is_active
    })
    
    return {
        "id": schedule.id,
        "is_active": schedule.is_active,
        "message": f"Schedule {'activated' if schedule.is_active else 'deactivated'} successfully"
    }
