from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables
    """
    # Import ALL models to ensure they are registered
    from app.db.models.user import User
    from app.db.models.business import Business
    from app.db.models.media import Media
    from app.db.models.schedule import Schedule
    
    # Create all tables
    Base.metadata.create_all(bind=engine)