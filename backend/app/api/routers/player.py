"""
Public Player API Routes
Endpoints públicos para el reproductor digital sin autenticación requerida
"""
from fastapi import APIRouter, Depends, HTTPException, Request
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
    Obtener todas las playlists (público para reproductor) con conteos correctos
    """
    playlists = playlist_crud.list_playlists(db, skip=skip, limit=limit)
    
    # Calcular media_count y total_duration para cada playlist
    playlists_with_counts = []
    for playlist in playlists:
        # Obtener elementos de la playlist
        playlist_items = playlist_crud.get_playlist_media(db, playlist_id=playlist.id)
        
        # Calcular duración total
        total_duration = 0
        for item in playlist_items:
            media = media_crud.get_media(db, media_id=item.media_id)
            if media and media.duration:
                total_duration += media.duration
        
        # Crear diccionario con los datos correctos
        playlist_dict = {
            "id": playlist.id,
            "name": playlist.name,
            "description": playlist.description,
            "created_at": playlist.created_at,
            "updated_at": playlist.updated_at,
            "media_count": len(playlist_items),
            "total_duration": total_duration
        }
        playlists_with_counts.append(playlist_dict)
    
    return playlists_with_counts

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
    
    # Usar la misma lógica que media.py para agregar URLs
    for media in media_files:
        import os
        served_filename = os.path.basename(media.filepath)
        media.file_url = f"/uploads/{served_filename}"
        media.served_filename = served_filename
    
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
    
    # Usar la misma lógica que media.py para agregar URLs
    import os
    served_filename = os.path.basename(media.filepath)
    media.file_url = f"/uploads/{served_filename}"
    media.served_filename = served_filename
    
    return media

@router.get("/playlists/{playlist_id}/complete")
async def get_public_playlist_complete(
    playlist_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Obtener playlist completa con todos los medios para el reproductor
    """
    # Verificar que la playlist existe
    playlist = playlist_crud.get_playlist(db, playlist_id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    # Obtener elementos de la playlist
    playlist_items = playlist_crud.get_playlist_media(db, playlist_id=playlist_id)
    
    # Construir base URL del servidor actual
    base_url = f"{request.url.scheme}://{request.url.netloc}"
    
    # Obtener información completa de cada media
    media_list = []
    for item in playlist_items:
        media = media_crud.get_media(db, media_id=item.media_id)
        if media:
            # Usar la misma lógica que media.py para construir URLs
            import os
            served_filename = os.path.basename(media.filepath)
            file_url = f"{base_url}/uploads/{served_filename}"  # URL completa
            
            media_dict = {
                "id": media.id,
                "filename": media.filename,
                "filepath": media.filepath,
                "media_type": media.media_type,
                "duration": media.duration,
                "created_at": media.created_at,
                "file_url": file_url,
                "served_filename": served_filename,
                "order_index": item.order_index,
                "playlist_media_id": item.id
            }
            media_list.append(media_dict)
    
    # Ordenar por order_index
    media_list.sort(key=lambda x: x["order_index"])
    
    # Preparar respuesta completa
    return {
        "id": playlist.id,
        "name": playlist.name,
        "description": playlist.description,
        "created_at": playlist.created_at,
        "updated_at": playlist.updated_at,
        "media_count": len(media_list),
        "total_duration": sum(m["duration"] or 0 for m in media_list),
        "medias": media_list  # Cambiar de "media" a "medias" para coincidir con el frontend
    }
