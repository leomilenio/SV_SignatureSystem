"""
Business router for business information management
"""
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
import base64
from typing import Optional

from app.db import get_db
from app.db.crud import business_crud
from app.db.schemas.business_schema import BusinessCreate, BusinessRead, BusinessUpdate
from app.api.routers.auth import get_current_user
from app.db.models.user import User

router = APIRouter()


@router.get("/", response_model=BusinessRead)
def get_business_info(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get business information (singleton pattern)"""
    business = business_crud.get_or_create_business(db)
    return business


@router.put("/", response_model=BusinessRead)
def update_business_info(
    name: Optional[str] = Form(None),
    logo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update business information"""
    logo_bytes = None
    if logo:
        logo_bytes = logo.file.read()
    
    # Only update fields that are provided
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if logo_bytes is not None:
        update_data["logo"] = logo_bytes
    
    # If no data to update, just return current business
    if not update_data:
        business = business_crud.get_or_create_business(db)
        return business
    
    business_update = BusinessUpdate(**update_data)
    
    business = business_crud.update_business(db, business_id=1, business_update=business_update)
    if not business:
        # If doesn't exist, create it with provided data or defaults
        business_create = BusinessCreate(
            name=name or "Mi Negocio",
            logo=logo_bytes
        )
        business = business_crud.create_business(db, business_create)
    
    return business


@router.get("/logo")
def get_business_logo(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get business logo as base64"""
    business = business_crud.get_business(db)
    if not business or not business.logo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Logo not found"
        )
    
    # Convert bytes to base64 for frontend consumption
    logo_b64 = base64.b64encode(business.logo).decode('utf-8')
    return {"logo": logo_b64}
