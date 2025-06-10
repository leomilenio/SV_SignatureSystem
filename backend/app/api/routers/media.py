"""
Media router for file upload and management
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.db.crud import media_crud
from app.db.schemas.media_schema import MediaCreate, MediaRead, MediaUpdate, MediaType
from app.api.routers.auth import get_current_user
from app.db.models.user import User

router = APIRouter()


@router.post("/", response_model=MediaRead)
async def create_media(
    filename: str = Form(...),
    media_type: MediaType = Form(...), 
    duration: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload new media file"""
    media_data = MediaCreate(
        filename=filename,
        media_type=media_type,
        duration=duration
    )
    
    try:
        return media_crud.create_media(db=db, media_in=media_data, file=file)
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
    current_user: User = Depends(get_current_user)
):
    """Update media duration"""
    media = media_crud.update_media(db, media_id=media_id, media_update=media_update)
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )
    return media


@router.delete("/{media_id}")
def delete_media(
    media_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete media file"""
    success = media_crud.delete_media(db, media_id=media_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )
    return {"message": "Media deleted successfully"}