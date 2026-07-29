#!/usr/bin/env python3
"""
Simulate traffic for Auth0 Flask App Monitoring Lab
Simulates valid and invalid accesses to test logging and alerts
"""

import requests
import time
import sys
from urllib.parse import urljoin

BASE_URL = "http://localhost:5000"

def test_public_access():
    """Test public endpoints (should work without login)"""
    print("\n=== Testing Public Access ===")
    
    # Test home page
    response = requests.get(urljoin(BASE_URL, "/"))
    print(f"Home Page: {response.status_code} - {'✅' if response.status_code == 200 else '❌'}")
    
    # Test health endpoint
    response = requests.get(urljoin(BASE_URL, "/health"))
    print(f"Health Endpoint: {response.status_code} - {'✅' if response.status_code == 200 else '❌'}")

def test_unauthorized_access():
    """Test protected endpoints without login (should redirect)"""
    print("\n=== Testing Unauthorized Access ===")
    
    # Test protected route without login
    response = requests.get(urljoin(BASE_URL, "/protected"), allow_redirects=False)
    print(f"Protected Route (Unauthorized): {response.status_code} - {'✅' if response.status_code == 302 else '❌'}")
    
    # Test profile without login
    response = requests.get(urljoin(BASE_URL, "/profile"), allow_redirects=False)
    print(f"Profile (Unauthorized): {response.status_code} - {'✅' if response.status_code == 302 else '❌'}")

def simulate_protected_access(session_cookie, num_accesses=20, delay=0.5):
    """
    Simulate multiple protected route accesses
    Args:
        session_cookie: Session cookie from browser (after login)
        num_accesses: Number of times to access
        delay: Delay between requests in seconds
    """
    print(f"\n=== Simulating {num_accesses} Protected Accesses ===")
    
    cookies = {'session': session_cookie} if session_cookie else {}
    success_count = 0
    fail_count = 0
    
    for i in range(num_accesses):
        try:
            response = requests.get(urljoin(BASE_URL, "/protected"), cookies=cookies)
            
            if response.status_code == 200:
                success_count += 1
                print(f"Access #{i+1}: 200 OK ✅")
            elif response.status_code == 302:
                fail_count += 1
                print(f"Access #{i+1}: 302 Redirect (Not logged in) ⚠️")
            else:
                fail_count += 1
                print(f"Access #{i+1}: {response.status_code} ❌")
            
            time.sleep(delay)
            
        except Exception as e:
            fail_count += 1
            print(f"Access #{i+1}: Error - {e} ❌")
    
    print(f"\nResults: {success_count} successful, {fail_count} failed")
    return success_count, fail_count

def main():
    """Main function to run all tests"""
    print("=" * 50)
    print("AUTH0 FLASK APP - TRAFFIC SIMULATOR")
    print("For Lab: Securing and Monitoring")
    print("=" * 50)
    
    # 1. Test public access
    test_public_access()
    
    # 2. Test unauthorized access
    test_unauthorized_access()
    
    # 3. Ask for session cookie
    print("\n" + "=" * 50)
    print("To simulate authenticated access, you need your session cookie.")
    print("1. Log in to the app at http://localhost:5000")
    print("2. Open browser Dev Tools (F12)")
    print("3. Go to Application/Storage -> Cookies -> localhost:5000")
    print("4. Copy the value of 'session' cookie")
    print("=" * 50)
    
    session_cookie = input("\nEnter session cookie (or press Enter to skip): ").strip()
    
    if session_cookie:
        # 4. Simulate protected access
        num_accesses = input("Number of accesses to simulate (default 20): ").strip()
        num_accesses = int(num_accesses) if num_accesses else 20
        
        delay = input("Delay between requests in seconds (default 1): ").strip()
        delay = float(delay) if delay else 1.0
        
        simulate_protected_access(session_cookie, num_accesses, delay)
    else:
        print("\nSkipping authenticated tests...")
    
    print("\n" + "=" * 50)
    print("Test completed! Check your terminal for SECURITY_EVENT logs.")
    print("For Azure monitoring, deploy your app and run these tests again.")
    print("=" * 50)

if __name__ == "__main__":
    main()
