"""Manual test script for authentication endpoints.

This module relies on the ``requests`` library and is intended to be
executed manually. If ``requests`` is not available, ``pytest`` will skip
this module during collection.
"""
import pytest

pytest.importorskip("requests")
import requests
import json

BASE_URL = "http://localhost:8002"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print("Health check:", response.json())

def test_check_setup():
    """Test setup check endpoint"""
    response = requests.get(f"{BASE_URL}/api/auth/check-setup")
    print("Setup check:", response.json())
    return response.json().get("setup_required", False)

def test_setup_admin():
    """Test admin setup"""
    admin_data = {
        "username": "admin",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/setup-admin", json=admin_data)
    print("Setup admin:", response.status_code, response.json())

def test_login():
    """Test login"""
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
    print("Login:", response.status_code, response.json())
    
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def test_protected_route(token):
    """Test protected route"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/auth/protected", headers=headers)
    print("Protected route:", response.status_code, response.json())

def test_me(token):
    """Test current user endpoint"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
    print("Current user:", response.status_code, response.json())

def test_logout(token):
    """Test logout"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/api/auth/logout", headers=headers)
    print("Logout:", response.status_code, response.json())

if __name__ == "__main__":
    print("=== Testing Authentication Module ===")
    
    # Test health
    test_health()
    
    # Check if setup is required
    setup_required = test_check_setup()
    
    # Setup admin if required
    if setup_required:
        test_setup_admin()
    
    # Test login
    token = test_login()
    
    if token:
        # Test protected routes
        test_protected_route(token)
        test_me(token)
        test_logout(token)
        
        # Test token after logout (should fail)
        print("\n=== Testing after logout ===")
        test_protected_route(token)
    
    print("\n=== Tests completed ===")
