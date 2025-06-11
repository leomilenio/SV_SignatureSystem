"""
Authentication router
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db import get_db
from app.core.security import create_access_token, verify_token, blacklist_token
from app.db.crud.user_crud import get_user_by_username, create_user, authenticate_user, count_users
from app.db.schemas.token_schema import Token
from app.db.schemas.user_schema import UserCreate, UserResponse
from app.config import settings

router = APIRouter()

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(current_user = Depends(get_current_user)):
    """Get current active user (for protected routes)"""
    return current_user


@router.post("/setup-admin", response_model=UserResponse)
def setup_admin(user_in: UserCreate, db: Session = Depends(get_db)):
    """Create the first and only admin user if no users exist"""
    if count_users(db) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin already exists"
        )
    
    # Check if username already exists (shouldn't happen if count is 0, but safety check)
    existing_user = get_user_by_username(db, user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    return create_user(db, user_in)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login endpoint - validates credentials and returns JWT token"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    """Logout endpoint - blacklist the token"""
    blacklist_token(token)
    return {"msg": "Logout successful"}


@router.get("/protected")
def protected_route(current_user = Depends(get_current_active_user)):
    """Example protected route that requires authentication"""
    return {
        "msg": "You are authenticated", 
        "user": current_user.username,
        "role": current_user.role
    }


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user = Depends(get_current_user)):
    """Get current user info"""
    return current_user


@router.get("/check-setup")
def check_admin_setup(db: Session = Depends(get_db)):
    """Check if admin setup is required"""
    user_count = count_users(db)
    return {
        "setup_required": user_count == 0,
        "user_count": user_count
    }
