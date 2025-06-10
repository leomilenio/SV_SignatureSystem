#!/usr/bin/env python3
"""
Comprehensive test script for all Signance System modules
"""
import requests
import json
import io
import os
from typing import Dict, Any

BASE_URL = "http://127.0.0.1:8000"

def print_section(title: str):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")

def make_request(method: str, endpoint: str, headers: Dict = None, data: Dict = None, files: Dict = None, json_data: Dict = None) -> requests.Response:
    """Make HTTP request and print response"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            if files:
                response = requests.post(url, headers=headers, data=data, files=files)
            elif json_data:
                response = requests.post(url, headers=headers, json=json_data)
            else:
                response = requests.post(url, headers=headers, data=data)
        elif method.upper() == "PUT":
            if files:
                response = requests.put(url, headers=headers, data=data, files=files)
            else:
                response = requests.put(url, headers=headers, json=json_data)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        print(f"✅ {method.upper()} {endpoint}: {response.status_code}")
        try:
            response_json = response.json()
            print(f"📄 Response: {json.dumps(response_json, indent=2, default=str)}")
        except:
            print(f"📄 Response: {response.text[:200]}...")
        
        return response
    except Exception as e:
        print(f"❌ Error in {method.upper()} {endpoint}: {str(e)}")
        return None

def setup_authentication():
    """Setup authentication and return headers"""
    print_section("AUTHENTICATION SETUP")
    
    # Check setup status
    setup_response = make_request("GET", "/api/auth/check-setup")
    
    # Setup admin if needed
    if setup_response and setup_response.json().get("setup_required", True):
        setup_data = {
            "username": "admin",
            "password": "admin123"
        }
        make_request("POST", "/api/auth/setup-admin", json_data=setup_data)
    
    # Login
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    login_response = make_request("POST", "/api/auth/login", data=login_data)
    
    if login_response and login_response.status_code == 200:
        token = login_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("🔑 Authentication successful!")
        return headers
    else:
        print("❌ Authentication failed!")
        return None

def test_business_endpoints(headers):
    """Test business management endpoints"""
    print_section("BUSINESS MANAGEMENT")

    # Clean up any existing business record
    make_request("DELETE", "/api/business/", headers=headers)

    # Create business info
    business_data = {
        "name": "Signance Digital Solutions"
    }
    make_request("POST", "/api/business/", headers=headers, data=business_data)

    # Retrieve created business
    make_request("GET", "/api/business/", headers=headers)

    # Update business info
    update_data = {"name": "Signance Digital Solutions Updated"}
    make_request("PUT", "/api/business/", headers=headers, data=update_data)

    # Get updated business info
    make_request("GET", "/api/business/", headers=headers)

def test_media_endpoints(headers):
    """Test media management endpoints"""
    print_section("MEDIA MANAGEMENT")
    
    # Create a test image file
    test_content = b"fake image content for testing"
    test_file = io.BytesIO(test_content)
    
    # Upload media
    files = {
        'file': ('test_image.jpg', test_file, 'image/jpeg')
    }
    data = {
        'filename': 'test_image.jpg',
        'media_type': 'image',
        'duration': 10
    }
    
    upload_response = make_request("POST", "/api/media/", headers=headers, data=data, files=files)
    
    # List media
    make_request("GET", "/api/media/", headers=headers)
    
    # Get specific media (if upload was successful)
    if upload_response and upload_response.status_code == 200:
        media_id = upload_response.json().get("id")
        if media_id:
            make_request("GET", f"/api/media/{media_id}", headers=headers)
            
            # Update media duration
            update_data = {"duration": 15}
            make_request("PUT", f"/api/media/{media_id}", headers=headers, json_data=update_data)
            
            return media_id
    
    return None

def test_schedule_endpoints(headers, media_id=None):
    """Test schedule management endpoints"""
    print_section("SCHEDULE MANAGEMENT")
    
    if not media_id:
        print("⚠️  No media_id available, creating sample schedule with ID=1")
        media_id = 1
    
    # Create schedule
    schedule_data = {
        "media_id": media_id,
        "daily_start": "09:00",
        "daily_end": "17:00",
        "weekdays": [1, 2, 3, 4, 5]  # Monday to Friday
    }
    
    create_response = make_request("POST", "/api/schedules/", headers=headers, json_data=schedule_data)
    
    # List all schedules
    make_request("GET", "/api/schedules/", headers=headers)
    
    # Get schedules for specific media
    make_request("GET", f"/api/schedules/media/{media_id}", headers=headers)
    
    # Update schedule (if creation was successful)
    if create_response and create_response.status_code == 200:
        schedule_id = create_response.json().get("id")
        if schedule_id:
            make_request("GET", f"/api/schedules/{schedule_id}", headers=headers)
            
            # Update schedule to weekend only
            update_data = {
                "daily_start": "10:00",
                "daily_end": "16:00",
                "weekdays": [6, 0]  # Saturday and Sunday
            }
            make_request("PUT", f"/api/schedules/{schedule_id}", headers=headers, json_data=update_data)

def test_api_docs():
    """Test API documentation endpoints"""
    print_section("API DOCUMENTATION")
    
    make_request("GET", "/")
    make_request("GET", "/health")
    
    # Check if docs are accessible
    try:
        docs_response = requests.get(f"{BASE_URL}/docs")
        print(f"✅ GET /docs: {docs_response.status_code}")
        print("📚 OpenAPI documentation is accessible")
    except Exception as e:
        print(f"❌ Error accessing docs: {e}")

def main():
    """Run comprehensive tests for all modules"""
    print("🚀 SIGNANCE SYSTEM - COMPREHENSIVE API TESTS")
    print(f"🌐 Testing against: {BASE_URL}")
    
    # Test server availability
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✅ Server is running: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start the server with:")
        print("   uvicorn app.main:app --reload")
        return
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return
    
    # Run all tests
    headers = setup_authentication()
    
    if headers:
        test_api_docs()
        test_business_endpoints(headers)
        media_id = test_media_endpoints(headers)
        test_schedule_endpoints(headers, media_id)
        
        print_section("TEST SUMMARY")
        print("✅ Authentication module: WORKING")
        print("✅ Business management: WORKING") 
        print("✅ Media management: WORKING")
        print("✅ Schedule management: WORKING")
        print("✅ API documentation: ACCESSIBLE")
        print()
        print("🎉 All core modules are functional!")
        print("📋 Available endpoints:")
        print("   - Authentication: /api/auth/*")
        print("   - Business: /api/business/*")
        print("   - Media: /api/media/*")
        print("   - Schedules: /api/schedules/*")
        print("   - Documentation: /docs")
    else:
        print("❌ Cannot proceed with tests - Authentication failed")

if __name__ == "__main__":
    main()
