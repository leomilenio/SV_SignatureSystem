"""
CRUD operations for Playlist
"""
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import func
from typing import List, Optional

from app.db.models.playlist import Playlist
from app.db.models.playlist_media import PlaylistMedia
from app.db.models.media import Media
from app.db.models.schedule import Schedule
from app.db.schemas.playlist_schema import PlaylistCreate, PlaylistUpdate, PlaylistStats
from app.db.schemas.playlist_media_schema import PlaylistAddMediaRequest, PlaylistReorderRequest


def create_playlist(db: Session, playlist_in: PlaylistCreate) -> Playlist:
    """Create new playlist"""
    db_playlist = Playlist(**playlist_in.dict())
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)
    return db_playlist


def get_playlist(db: Session, playlist_id: int) -> Optional[Playlist]:
    """Get playlist by ID with media"""
    return db.query(Playlist)\
        .options(selectinload(Playlist.playlist_media).selectinload(PlaylistMedia.media))\
        .filter(Playlist.id == playlist_id).first()


def list_playlists(db: Session, skip: int = 0, limit: int = 100) -> List[Playlist]:
    """List playlists with pagination and media"""
    return db.query(Playlist)\
        .options(selectinload(Playlist.playlist_media).selectinload(PlaylistMedia.media))\
        .offset(skip).limit(limit).all()


def update_playlist(db: Session, playlist_id: int, playlist_update: PlaylistUpdate) -> Optional[Playlist]:
    """Update playlist record"""
    db_playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not db_playlist:
        return None
    
    update_data = playlist_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_playlist, field, value)
    
    db.commit()
    db.refresh(db_playlist)
    return db_playlist


def delete_playlist(db: Session, playlist_id: int) -> bool:
    """Delete playlist record"""
    db_playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not db_playlist:
        return False
    
    db.delete(db_playlist)
    db.commit()
    return True


def get_playlist_stats(db: Session) -> PlaylistStats:
    """Get playlist statistics"""
    try:
        total_playlists = db.query(Playlist).count()
        
        # Importar Schedule localmente para evitar problemas circulares
        from app.db.models.schedule import Schedule
        total_scheduled_items = db.query(Schedule).count()
        
        return PlaylistStats(
            total_playlists=total_playlists,
            total_scheduled_items=total_scheduled_items
        )
    except Exception as e:
        print(f"Error getting playlist stats: {e}")
        # Retornar stats por defecto en caso de error
        return PlaylistStats(
            total_playlists=0,
            total_scheduled_items=0
        )


def add_single_media_to_playlist(db: Session, playlist_id: int, media_id: int, duration: Optional[int] = None) -> bool:
    """Add a single media to playlist with optional custom duration"""
    try:
        # Verificar que la playlist existe
        playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
        if not playlist:
            return False
        
        # Verificar que el media existe
        media = db.query(Media).filter(Media.id == media_id).first()
        if not media:
            return False
        
        # Verificar que no existe ya la relación
        existing = db.query(PlaylistMedia).filter(
            PlaylistMedia.playlist_id == playlist_id,
            PlaylistMedia.media_id == media_id
        ).first()
        if existing:
            return False
        
        # Obtener el siguiente order_index
        max_order = db.query(func.max(PlaylistMedia.order_index))\
            .filter(PlaylistMedia.playlist_id == playlist_id).scalar()
        order_index = (max_order + 1) if max_order is not None else 0
        
        # Crear la relación
        playlist_media = PlaylistMedia(
            playlist_id=playlist_id,
            media_id=media_id,
            order_index=order_index,
            duration=duration
        )
        db.add(playlist_media)
        db.commit()
        return True
    except Exception as e:
        print(f"Error adding single media to playlist: {e}")
        db.rollback()
        return False


def add_media_to_playlist(db: Session, request: PlaylistAddMediaRequest) -> bool:
    """Add multiple media to playlist"""
    try:
        # Verificar que la playlist existe
        playlist = db.query(Playlist).filter(Playlist.id == request.playlist_id).first()
        if not playlist:
            return False
        
        # Obtener el order_index inicial
        max_order = db.query(func.max(PlaylistMedia.order_index))\
            .filter(PlaylistMedia.playlist_id == request.playlist_id).scalar()
        next_order = (max_order + 1) if max_order is not None else 0
        
        # Agregar cada medio
        for media_id in request.media_ids:
            # Verificar que el media existe
            media = db.query(Media).filter(Media.id == media_id).first()
            if not media:
                continue
            
            # Verificar que no existe ya la relación
            existing = db.query(PlaylistMedia).filter(
                PlaylistMedia.playlist_id == request.playlist_id,
                PlaylistMedia.media_id == media_id
            ).first()
            if existing:
                continue
            
            # Crear la relación
            playlist_media = PlaylistMedia(
                playlist_id=request.playlist_id,
                media_id=media_id,
                order_index=next_order
            )
            db.add(playlist_media)
            next_order += 1
        
        db.commit()
        return True
    except Exception as e:
        print(f"Error adding media to playlist: {e}")
        db.rollback()
        return False


def remove_media_from_playlist(db: Session, playlist_id: int, media_id: int) -> bool:
    """Remove media from playlist"""
    try:
        playlist_media = db.query(PlaylistMedia).filter(
            PlaylistMedia.playlist_id == playlist_id,
            PlaylistMedia.media_id == media_id
        ).first()
        
        if not playlist_media:
            return False
        
        db.delete(playlist_media)
        db.commit()
        return True
    except Exception as e:
        print(f"Error removing media from playlist: {e}")
        db.rollback()
        return False


def reorder_playlist_media(db: Session, request: PlaylistReorderRequest) -> bool:
    """Reorder media in playlist"""
    try:
        # Actualizar el order_index de cada media en la playlist
        for media_order in request.media_order:
            db.query(PlaylistMedia).filter(
                PlaylistMedia.playlist_id == request.playlist_id,
                PlaylistMedia.media_id == media_order.media_id
            ).update({"order_index": media_order.order_index})
        
        db.commit()
        return True
    except Exception as e:
        print(f"Error reordering playlist media: {e}")
        db.rollback()
        return False


def get_playlist_media(db: Session, playlist_id: int) -> List[PlaylistMedia]:
    """Get ordered media in playlist"""
    return db.query(PlaylistMedia)\
        .options(selectinload(PlaylistMedia.media))\
        .filter(PlaylistMedia.playlist_id == playlist_id)\
        .order_by(PlaylistMedia.order_index).all()


def get_playlist_media_relation(db: Session, playlist_id: int, media_id: int) -> Optional[PlaylistMedia]:
    """Get the PlaylistMedia relation between a playlist and media"""
    return db.query(PlaylistMedia)\
        .filter(
            PlaylistMedia.playlist_id == playlist_id,
            PlaylistMedia.media_id == media_id
        ).first()


def update_media_duration_in_playlist(db: Session, playlist_id: int, media_id: int, duration: int) -> bool:
    """Update the duration of a specific media in a playlist"""
    playlist_media = db.query(PlaylistMedia)\
        .filter(
            PlaylistMedia.playlist_id == playlist_id,
            PlaylistMedia.media_id == media_id
        ).first()
    
    if not playlist_media:
        return False
    
    playlist_media.duration = duration
    db.commit()
    return True
