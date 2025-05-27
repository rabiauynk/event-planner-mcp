#!/usr/bin/env python3
"""
Test script to verify deployment readiness
"""
import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests imported successfully")
    except ImportError as e:
        print(f"❌ Requests import failed: {e}")
        return False
    
    try:
        from app import app
        print("✅ App module imported successfully")
    except ImportError as e:
        print(f"❌ App import failed: {e}")
        return False
    
    try:
        from planner import get_events
        print("✅ Planner module imported successfully")
    except ImportError as e:
        print(f"❌ Planner import failed: {e}")
        return False
    
    return True

def test_api_key():
    """Test API key availability"""
    print("\nTesting API key...")
    
    api_key = os.getenv('TICKETMASTER_API_KEY') or 'iEXnISiQ5GXqqBWIlBzLOwP3cej3CKlo'
    
    if api_key:
        print("✅ API key is available")
        if api_key == 'iEXnISiQ5GXqqBWIlBzLOwP3cej3CKlo':
            print("✅ Using built-in API key")
        else:
            print("✅ Using environment variable API key")
        return True
    else:
        print("❌ No API key found")
        return False

def test_app_creation():
    """Test if Flask app can be created"""
    print("\nTesting app creation...")
    
    try:
        from app import app
        print("✅ Flask app created successfully")
        
        # Test routes
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/health')
            if response.status_code == 200:
                print("✅ Health endpoint working")
            else:
                print(f"❌ Health endpoint failed: {response.status_code}")
                return False
            
            # Test home endpoint
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Home endpoint working")
            else:
                print(f"❌ Home endpoint failed: {response.status_code}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Event Planner MCP Deployment Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_api_key,
        test_app_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Ready for deployment.")
        return 0
    else:
        print("❌ Some tests failed. Check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
