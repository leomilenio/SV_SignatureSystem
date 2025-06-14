"""
Playlist router for playlist management
"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.api.routers.auth import get_current_user
from app.db.models.user import User
from app.core.websocket_manager import broadcast_event

router = APIRouter()

# Importación local para evitar problemas circulares
def get_playlist_crud():
    from app.db.crud import playlist_crud
    return playlist_crud

def get_playlist_schemas():
    from app.db.schemas.playlist_schema import PlaylistCreate, PlaylistRead, PlaylistUpdate, PlaylistStats
    return PlaylistCreate, PlaylistRead, PlaylistUpdate, PlaylistStats


@router.get("/", response_model=List[dict])
def list_playlists(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all playlists"""
    crud = get_playlist_crud()
    playlists = crud.list_playlists(db, skip=skip, limit=limit)
    
    # Convertir a dict para evitar problemas de serialización
    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "created_at": p.created_at.isoformat() if p.created_at else None,
            "updated_at": p.updated_at.isoformat() if p.updated_at else None,
            # contar medios asociados a la playlist
            "media_count": len(p.playlist_media) if hasattr(p, 'playlist_media') else 0,
            # duración total de la playlist (suma de duraciones efectivas)
            "total_duration": sum(
                (pm.duration if pm.duration is not None else pm.media.duration)
                for pm in getattr(p, 'playlist_media', [])
            )
        }
        for p in playlists
    ]


@router.get("/stats")
def get_playlist_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get playlist statistics"""
    crud = get_playlist_crud()
    stats = crud.get_playlist_stats(db)
    
    return {
        "total_playlists": stats.total_playlists,
        "total_scheduled_items": stats.total_scheduled_items
    }


@router.post("/")
def create_playlist(
    playlist_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new playlist"""
    crud = get_playlist_crud()
    PlaylistCreate, _, _, _ = get_playlist_schemas()
    
    playlist_in = PlaylistCreate(**playlist_data)
    new_playlist = crud.create_playlist(db=db, playlist_in=playlist_in)
    
    return {
        "id": new_playlist.id,
        "name": new_playlist.name,
        "description": new_playlist.description,
        "created_at": new_playlist.created_at.isoformat() if new_playlist.created_at else None,
        "updated_at": new_playlist.updated_at.isoformat() if new_playlist.updated_at else None,
    }


@router.get("/{playlist_id}")
def get_playlist(
    playlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific playlist by ID with its media"""
    crud = get_playlist_crud()
    playlist = crud.get_playlist(db, playlist_id=playlist_id)
    
    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found"
        )
    
    # Obtener medios ordenados de la playlist
    playlist_medias = crud.get_playlist_media(db, playlist_id)
    media_list = []
    total_duration = 0
    
    for pm in playlist_medias:
        # Usar la duración específica de la playlist o la original del media
        effective_duration = pm.duration if pm.duration is not None else pm.media.duration
        
        # Corregir filepath para servir archivos correctamente
        filepath = pm.media.filepath
        if filepath and not filepath.startswith('/uploads/'):
            filepath = f'/uploads/{filepath}'
        
        media_data = {
            "id": pm.media.id,
            "filename": pm.media.filename,
            "filepath": filepath,
            "media_type": pm.media.media_type,
            "duration": pm.media.duration,
            "playlist_duration": pm.duration,
            "effective_duration": effective_duration,
            "order_index": pm.order_index,
            "added_at": pm.added_at.isoformat() if pm.added_at else None
        }
        media_list.append(media_data)
        total_duration += effective_duration
    
    return {
        "id": playlist.id,
        "name": playlist.name,
        "description": playlist.description,
        "created_at": playlist.created_at.isoformat() if playlist.created_at else None,
        "updated_at": playlist.updated_at.isoformat() if playlist.updated_at else None,
        "media_count": len(media_list),
        "total_duration": total_duration,
        "medias": media_list
    }


@router.put("/{playlist_id}")
def update_playlist(
    playlist_id: int,
    playlist_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update playlist"""
    crud = get_playlist_crud()
    _, _, PlaylistUpdate, _ = get_playlist_schemas()
    
    playlist_update = PlaylistUpdate(**playlist_data)
    playlist = crud.update_playlist(
        db, playlist_id=playlist_id, playlist_update=playlist_update
    )
    
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


@router.delete("/{playlist_id}")
def delete_playlist(
    playlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete playlist"""
    crud = get_playlist_crud()
    success = crud.delete_playlist(db, playlist_id=playlist_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found"
        )
    
    return {"message": "Playlist deleted successfully"}


@router.post("/{playlist_id}/media")
async def add_media_to_playlist(
    playlist_id: int,
    media_data: dict,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add media to playlist"""
    crud = get_playlist_crud()
    
    # Importar schemas localmente
    from app.db.schemas.playlist_media_schema import PlaylistAddMediaRequest, PlaylistAddSingleMediaRequest
    
    # Determinar si es un solo medio o múltiples medios
    if 'media_id' in media_data:
        # Caso: agregar un solo medio
        request = PlaylistAddSingleMediaRequest(**media_data)
        success = crud.add_single_media_to_playlist(db, playlist_id, request.media_id, request.duration)
    elif 'media_ids' in media_data:
        # Caso: agregar múltiples medios
        request_data = media_data.copy()
        request_data["playlist_id"] = playlist_id
        request = PlaylistAddMediaRequest(**request_data)
        success = crud.add_media_to_playlist(db, request)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either 'media_id' or 'media_ids' must be provided"
        )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not add media to playlist"
        )
    
    # Notificar actualización de playlist vía WebSocket
    background_tasks.add_task(broadcast_event, "playlist_updated", {
        "playlist_id": playlist_id,
        "action": "media_added"
    })
    
    return {"message": "Media added to playlist successfully"}


@router.delete("/{playlist_id}/media/{media_id}")
async def remove_media_from_playlist(
    playlist_id: int,
    media_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove media from playlist"""
    crud = get_playlist_crud()
    success = crud.remove_media_from_playlist(db, playlist_id, media_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found in playlist"
        )
    
    # Notificar actualización de playlist vía WebSocket
    background_tasks.add_task(broadcast_event, "playlist_updated", {
        "playlist_id": playlist_id,
        "action": "media_removed",
        "media_id": media_id
    })
    
    return {"message": "Media removed from playlist successfully"}
