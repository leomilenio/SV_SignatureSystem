"""
Media router for file upload and management
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import os
from pathlib import Path

from app.db import get_db
from app.db.crud import media_crud
from app.db.schemas.media_schema import MediaCreate, MediaRead, MediaUpdate, MediaType
from app.api.routers.auth import get_current_user
from app.db.models.user import User
from app.utils import ffmpeg
from app.core.websocket_manager import broadcast_event

router = APIRouter()


@router.post("/", response_model=MediaRead)
async def create_media(
    filename: str = Form(...),
    media_type: MediaType = Form(...),
    duration: int = Form(...),  # Este valor será sobrescrito por la metadata real
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Upload new media file (image or video). Obtiene metadata real y genera thumbnail si es video."""
    try:
        # 1. Guardar archivo subido
        saved_filepath = media_crud.save_upload_file(file)
        saved_path = Path(saved_filepath)

        # 2. Obtener metadata real
        real_duration = duration
        extra_metadata = {}
        if media_type == MediaType.video:
            info = ffmpeg.get_media_info(saved_path)
            real_duration = int(info.get('duration', duration))
            extra_metadata = {
                'format': info.get('format'),
                'size': info.get('size'),
                'streams': info.get('streams')
            }
            # 3. Generar thumbnail para video
            thumb_path = saved_path.parent / f"{saved_path.stem}_thumb.jpg"
            ffmpeg.generate_thumbnail(saved_path, thumb_path, time_offset=1.0)
        else:
            # Si es imagen, solo obtener tamaño de archivo
            extra_metadata = {'size': saved_path.stat().st_size}

        # 4. Crear registro en base de datos con metadata real
        media_data = MediaCreate(
            filename=filename,
            media_type=media_type,
            duration=real_duration
        )
        db_media = media_crud.create_media(db=db, media_in=media_data, file=None, filepath_override=saved_filepath)
        background_tasks.add_task(broadcast_event, "media_created", {"id": db_media.id})

        # 5. (Opcional) Guardar metadata extra en un campo adicional si lo deseas
        # Por ahora solo se retorna en la respuesta
        response = db_media.__dict__.copy()
        response.update(extra_metadata)
        if media_type == MediaType.video:
            response['thumbnail'] = str(thumb_path)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading file: {str(e)}"
        )


@router.get("/", response_model=List[MediaRead])
def list_media(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all media files"""
    return media_crud.list_media(db, skip=skip, limit=limit)


@router.get("/{media_id}", response_model=MediaRead)
def get_media(
    media_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific media by ID"""
    media = media_crud.get_media(db, media_id=media_id)
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )
    return media


@router.put("/{media_id}", response_model=MediaRead)
def update_media(
    media_id: int,
    media_update: MediaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Update media duration"""
    media = media_crud.update_media(db, media_id=media_id, media_update=media_update)
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )
    background_tasks.add_task(broadcast_event, "media_updated", {"id": media.id})
    return media


@router.delete("/{media_id}")
def delete_media(
    media_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Delete media file"""
    success = media_crud.delete_media(db, media_id=media_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )
    background_tasks.add_task(broadcast_event, "media_deleted", {"id": media_id})
    return {"message": "Media deleted successfully"}