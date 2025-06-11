"""
Business router for business information management
"""
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form, BackgroundTasks
from sqlalchemy.orm import Session
import base64
from typing import Optional

from app.db import get_db
from app.db.crud import business_crud
from app.db.schemas.business_schema import BusinessCreate, BusinessRead, BusinessUpdate
from app.api.routers.auth import get_current_user
from app.db.models.user import User
from app.core.websocket_manager import broadcast_event

router = APIRouter()


@router.get("/", response_model=BusinessRead)
def get_business_info(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get business information (singleton pattern)"""
    business = business_crud.get_or_create_business(db)
    return business


@router.get("/check-setup")
def check_business_setup(db: Session = Depends(get_db)):
    """Check if business info exists"""
    exists = business_crud.get_business(db) is not None
    return {"setup_required": not exists}


@router.post("/", response_model=BusinessRead, status_code=status.HTTP_201_CREATED)
async def create_business_info(
    name: str = Form(...),
    logo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Create business information"""
    if business_crud.get_business(db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Business already exists")

    logo_bytes = logo.file.read() if logo else None

    business_create = BusinessCreate(name=name, logo=logo_bytes)
    business = business_crud.create_business(db, business_create)
    background_tasks.add_task(broadcast_event, "business_created", {"id": business.id})
    return business


@router.put("/", response_model=BusinessRead)
def update_business_info(
    name: Optional[str] = Form(None),
    logo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
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
    
    background_tasks.add_task(broadcast_event, "business_updated", {"id": business.id})
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


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_business(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Delete business record"""
    success = business_crud.delete_business(db, business_id=1)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found")
    background_tasks.add_task(broadcast_event, "business_deleted", {"id": 1})
    return None
