"""
User CRUD operations
"""
from typing import Optional
from sqlalchemy.orm import Session

from app.db.models.user import User
from app.db.schemas.user_schema import UserCreate
from app.core.security import get_password_hash, verify_password


def count_users(db: Session) -> int:
    """Count total number of users"""
    return db.query(User).count()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get user by username"""
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user_in: UserCreate) -> User:
    """Create a new user"""
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        username=user_in.username,
        hashed_password=hashed_password,
        role="admin"  # First user is always admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Authenticate user with username and password"""
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
