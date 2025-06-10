"""
CRUD operations for Business
"""
from sqlalchemy.orm import Session
from typing import Optional

from app.db.models.business import Business
from app.db.schemas.business_schema import BusinessCreate, BusinessUpdate


def get_business(db: Session, business_id: int = 1) -> Optional[Business]:
    """Get business by ID (default to ID=1 for singleton pattern)"""
    return db.query(Business).filter(Business.id == business_id).first()


def get_or_create_business(db: Session) -> Business:
    """Get existing business or create default one (singleton pattern)"""
    business = get_business(db)
    if not business:
        business = Business(name="Mi Negocio")
        db.add(business)
        db.commit()
        db.refresh(business)
    return business


def create_business(db: Session, business_in: BusinessCreate) -> Business:
    """Create new business record"""
    db_business = Business(**business_in.dict())
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    return db_business


def update_business(db: Session, business_id: int, business_update: BusinessUpdate) -> Optional[Business]:
    """Update business record"""
    db_business = get_business(db, business_id)
    if not db_business:
        return None
    
    update_data = business_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_business, field, value)
    
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    return db_business


def delete_business(db: Session, business_id: int) -> bool:
    """Delete business record"""
    db_business = get_business(db, business_id)
    if not db_business:
        return False
    
    db.delete(db_business)
    db.commit()
    return True
