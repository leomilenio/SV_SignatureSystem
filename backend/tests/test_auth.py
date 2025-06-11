import os
import sys
from pathlib import Path
import pytest

# Ensure dependencies from the provided virtual environment are available
VENVPATH = Path(__file__).resolve().parents[1] / "venv" / "lib" / "python3.11" / "site-packages"
if VENVPATH.exists():
    sys.path.append(str(VENVPATH))

# Add project root so ``import app`` works
ROOTPATH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOTPATH))

PROJECT_ROOT = ROOTPATH.parent
# Ensure upload directory exists before app import
UPLOAD_DIR = PROJECT_ROOT / "media" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

from fastapi.testclient import TestClient

# Use a temporary SQLite database for testing
TEST_DB = Path("./test.db")
if TEST_DB.exists():
    TEST_DB.unlink()
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"

from app.main import app
from app.db import init_db

# Initialize the database schema for tests
init_db()

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_auth_flow(client):
    # Health endpoint
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"

    # Check if admin setup is required
    r = client.get("/api/auth/check-setup")
    assert r.status_code == 200
    assert r.json()["setup_required"] is True

    # Create admin user
    payload = {"username": "admin", "password": "admin123"}
    r = client.post("/api/auth/setup-admin", json=payload)
    assert r.status_code == 200
    assert r.json()["username"] == "admin"

    # Login
    r = client.post("/api/auth/login", data=payload)
    assert r.status_code == 200
    token = r.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Access protected route
    r = client.get("/api/auth/protected", headers=headers)
    assert r.status_code == 200
    assert r.json()["user"] == "admin"

    # Current user endpoint
    r = client.get("/api/auth/me", headers=headers)
    assert r.status_code == 200
    assert r.json()["username"] == "admin"

    # Logout
    r = client.post("/api/auth/logout", headers=headers)
    assert r.status_code == 200

    # Token should be blacklisted now
    r = client.get("/api/auth/protected", headers=headers)
    assert r.status_code == 401
