"""
Public Player API Routes
Endpoints públicos para el reproductor digital sin autenticación requerida
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ...db.database import get_db
from ...db.crud import playlist_crud, media_crud
from ...db.schemas.playlist_schema import PlaylistRead
from ...db.schemas.media_schema import MediaRead
from ...db.schemas.playlist_media_schema import PlaylistMediaRead

router = APIRouter(prefix="/player", tags=["player"])

@router.get("/playlists", response_model=List[PlaylistRead])
async def get_public_playlists(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtener todas las playlists (público para reproductor)
    """
    playlists = playlist_crud.list_playlists(db, skip=skip, limit=limit)
    return playlists

@router.get("/playlists/{playlist_id}", response_model=PlaylistRead)
async def get_public_playlist(
    playlist_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener una playlist específica (público para reproductor)
    """
    playlist = playlist_crud.get_playlist(db, playlist_id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return playlist

@router.get("/playlists/{playlist_id}/items", response_model=List[PlaylistMediaRead])
async def get_public_playlist_items(
    playlist_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener elementos de una playlist (público para reproductor)
    """
    # Verificar que la playlist existe
    playlist = playlist_crud.get_playlist(db, playlist_id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    # Obtener elementos de la playlist
    items = playlist_crud.get_playlist_media(db, playlist_id=playlist_id)
    return items

@router.get("/media", response_model=List[MediaRead])
async def get_public_media(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtener archivos multimedia (público para reproductor)
    """
    media_files = media_crud.list_media(db, skip=skip, limit=limit)
    return media_files

@router.get("/media/{media_id}", response_model=MediaRead)
async def get_public_media_item(
    media_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener un archivo multimedia específico (público para reproductor)
    """
    media = media_crud.get_media(db, media_id=media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    return media
