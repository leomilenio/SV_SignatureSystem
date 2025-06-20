"""
CRUD operations for Media
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
import os
import uuid
from fastapi import UploadFile

from app.db.models.media import Media
from app.db.schemas.media_schema import MediaCreate, MediaUpdate
from app.config import settings


def save_upload_file(file: UploadFile) -> str:
    """Save uploaded file and return filepath"""
    # Generar nombre único
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else ''
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    
    # Asegurar que el directorio existe
    upload_dir = settings.UPLOAD_DIR
    os.makedirs(upload_dir, exist_ok=True)
    
    # Guardar archivo
    filepath = os.path.join(upload_dir, unique_filename)
    with open(filepath, "wb") as buffer:
        content = file.file.read()
        buffer.write(content)
    
    # Devolver filepath relativo para servir archivos (sin el "media" inicial)
    return f"/uploads/{unique_filename}"


def create_media(db: Session, media_in: MediaCreate, file: UploadFile = None, filepath_override: str = None) -> Media:
    """Create new media record. Si se pasa filepath_override, no guarda el archivo de nuevo."""
    if filepath_override:
        filepath = filepath_override
    else:
        filepath = save_upload_file(file)
    db_media = Media(
        filename=media_in.filename,
        filepath=filepath,
        media_type=media_in.media_type,
        duration=media_in.duration
    )
    
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return db_media


def get_media(db: Session, media_id: int) -> Optional[Media]:
    """Get media by ID"""
    return db.query(Media).filter(Media.id == media_id).first()


def list_media(db: Session, skip: int = 0, limit: int = 100) -> List[Media]:
    """List media with pagination"""
    return db.query(Media).offset(skip).limit(limit).all()


def update_media(db: Session, media_id: int, media_update: MediaUpdate) -> Optional[Media]:
    """Update media record"""
    db_media = get_media(db, media_id)
    if not db_media:
        return None
    
    update_data = media_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_media, field, value)
    
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return db_media


def delete_media(db: Session, media_id: int) -> bool:
    """Delete media record and associated file"""
    db_media = get_media(db, media_id)
    if not db_media:
        return False
    
    # Primero eliminar o actualizar las referencias en schedules
    from app.db.models.schedule import Schedule
    schedules_with_media = db.query(Schedule).filter(Schedule.media_id == media_id).all()
    
    for schedule in schedules_with_media:
        # Eliminar el schedule completo ya que el media asociado será eliminado
        db.delete(schedule)
    
    # Eliminar relaciones en playlist_media
    from app.db.models.playlist_media import PlaylistMedia
    playlist_media_relations = db.query(PlaylistMedia).filter(PlaylistMedia.media_id == media_id).all()
    for relation in playlist_media_relations:
        db.delete(relation)
    
    # Construir la ruta completa del archivo para eliminarlo
    # db_media.filepath es algo como "/uploads/filename.ext"
    # Necesitamos construir la ruta completa del sistema de archivos
    if db_media.filepath:
        # Extraer solo el nombre del archivo de la ruta
        filename_only = os.path.basename(db_media.filepath)
        # Construir la ruta completa usando UPLOAD_DIR
        full_file_path = os.path.join(settings.UPLOAD_DIR, filename_only)
        
        # Eliminar archivo físico si existe
        if os.path.exists(full_file_path):
            try:
                os.remove(full_file_path)
                print(f"✅ Archivo eliminado: {full_file_path}")
            except Exception as e:
                print(f"⚠️  Error eliminando archivo {full_file_path}: {e}")
        else:
            print(f"⚠️  Archivo no encontrado para eliminar: {full_file_path}")
        
        # También eliminar thumbnail si es un video (patrón: filename_thumb.jpg)
        if db_media.media_type == 'video':
            # Extraer nombre base sin extensión
            base_name = os.path.splitext(filename_only)[0]
            thumbnail_filename = f"{base_name}_thumb.jpg"
            thumbnail_path = os.path.join(settings.UPLOAD_DIR, thumbnail_filename)
            
            if os.path.exists(thumbnail_path):
                try:
                    os.remove(thumbnail_path)
                    print(f"✅ Thumbnail eliminado: {thumbnail_path}")
                except Exception as e:
                    print(f"⚠️  Error eliminando thumbnail {thumbnail_path}: {e}")
            else:
                print(f"⚠️  Thumbnail no encontrado: {thumbnail_path}")
    
    # Finalmente eliminar el registro de media
    db.delete(db_media)
    db.commit()
    return True


def get_media_playlists(db: Session, media_id: int):
    """Get all playlists that contain a specific media with order and duration info"""
    from app.db.models.playlist import Playlist
    from app.db.models.playlist_media import PlaylistMedia
    
    result = db.execute(
        select(
            Playlist.id,
            Playlist.name,
            Playlist.description,
            PlaylistMedia.order_index,
            PlaylistMedia.duration
        )
        .join(PlaylistMedia, Playlist.id == PlaylistMedia.playlist_id)
        .where(PlaylistMedia.media_id == media_id)
        .order_by(Playlist.name)
    )
    
    playlists = []
    for row in result:
        playlists.append({
            'id': row.id,
            'name': row.name,
            'description': row.description,
            'order_index': row.order_index,
            'duration': row.duration
        })
    
    return playlists
