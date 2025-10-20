#!/usr/bin/env python3

"""
Test all HTTP endpoints to verify they work correctly
"""

import requests
import json
import time

def test_http_endpoints():
    """Test all HTTP service endpoints"""
    base_url = "http://localhost:8888"
    
    print("HTTP Service Endpoint Test Suite")
    print("=" * 40)
    
    # Test endpoints
    test_cases = [
        {
            'name': 'Help',
            'url': f'{base_url}/help',
            'method': 'GET',
            'expected_status': 200
        },
        {
            'name': 'Status',
            'url': f'{base_url}/status',
            'method': 'GET',
            'expected_status': 200
        },
        {
            'name': 'Basic Message',
            'url': f'{base_url}/AlphaSign?msg=Hello World',
            'method': 'GET',
            'expected_status': 200
        },
        {
            'name': 'Formatted Message',
            'url': f'{base_url}/AlphaSign?msg=Test&color=red&effect=flash&speed=5',
            'method': 'GET',
            'expected_status': 200
        },
        {
            'name': 'Set Time',
            'url': f'{base_url}/settime?time=14:30',
            'method': 'GET',
            'expected_status': 200
        },
        {
            'name': 'Set Date',
            'url': f'{base_url}/setdate?date=12/25/23',
            'method': 'GET',
            'expected_status': 200
        },
        {
            'name': 'Sound Control',
            'url': f'{base_url}/sound?on=true',
            'method': 'GET',
            'expected_status': 200
        },
        {
            'name': 'Soft Reset',
            'url': f'{base_url}/reset',
            'method': 'GET',
            'expected_status': 200
        },
        {
            'name': 'Memory Info',
            'url': f'{base_url}/memory?action=info',
            'method': 'GET',
            'expected_status': 200
        },
        {
            'name': 'Memory Configure',
            'url': f'{base_url}/memory?action=configure',
            'method': 'GET',
            'expected_status': 200
        },
        {
            'name': 'Generate Tone',
            'url': f'{base_url}/tone?type=beep&freq=1000&duration=5',
            'method': 'GET',
            'expected_status': 200
        },
        {
            'name': 'Run Time Table',
            'url': f'{base_url}/runtime?label=A&start=09:00&stop=17:00',
            'method': 'GET',
            'expected_status': 200
        },
        {
            'name': 'Display Text at XY',
            'url': f'{base_url}/display?enabled=true&x=10&y=5&text=Hello',
            'method': 'GET',
            'expected_status': 200
        },
        {
            'name': 'Dimming Register',
            'url': f'{base_url}/dimming?action=register&dim=1&brightness=80',
            'method': 'GET',
            'expected_status': 200
        },
        {
            'name': 'Dimming Time',
            'url': f'{base_url}/dimming?action=time&start=18&stop=6',
            'method': 'GET',
            'expected_status': 200
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"{i:2d}. Testing {test_case['name']}...")
        
        try:
            if test_case['method'] == 'GET':
                response = requests.get(test_case['url'], timeout=5)
            else:
                response = requests.post(test_case['url'], timeout=5)
            
            status_ok = response.status_code == test_case['expected_status']
            
            if status_ok:
                print(f"    [OK] Status: {response.status_code}")
                
                # Try to parse JSON response
                try:
                    json_data = response.json()
                    if 'status' in json_data:
                        print(f"    [OK] Response: {json_data.get('status', 'unknown')}")
                    else:
                        print(f"    [OK] Response: {len(response.text)} characters")
                except:
                    print(f"    [OK] Response: {len(response.text)} characters")
                
                results.append(True)
            else:
                print(f"    [ERROR] Expected {test_case['expected_status']}, got {response.status_code}")
                print(f"    [ERROR] Response: {response.text[:100]}...")
                results.append(False)
                
        except requests.exceptions.ConnectionError:
            print(f"    [ERROR] Connection failed - is the service running?")
            results.append(False)
        except requests.exceptions.Timeout:
            print(f"    [ERROR] Request timeout")
            results.append(False)
        except Exception as e:
            print(f"    [ERROR] {str(e)}")
            results.append(False)
        
        print()
    
    # Summary
    total_tests = len(test_cases)
    passed_tests = sum(results)
    success_rate = (passed_tests / total_tests) * 100
    
    print("=" * 40)
    print("TEST SUMMARY")
    print("=" * 40)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("\n[SUCCESS] All HTTP endpoints working correctly!")
        print("The HTTP service is ready for production use.")
    elif success_rate >= 90:
        print("\n[GOOD] Most endpoints working correctly!")
        print("Minor issues may need attention.")
    else:
        print("\n[WARNING] Several endpoints have issues!")
        print("Review the errors above and fix the problems.")
    
    return success_rate == 100

def test_advanced_features():
    """Test advanced features with various parameters"""
    print("\nAdvanced Features Test")
    print("=" * 30)
    
    base_url = "http://localhost:8888"
    
    advanced_tests = [
        {
            'name': 'Custom Tone',
            'url': f'{base_url}/tone?type=custom&freq=2000&duration=3&repeat=2'
        },
        {
            'name': 'Alarm Tone',
            'url': f'{base_url}/tone?type=alarm'
        },
        {
            'name': 'Complex Message',
            'url': f'{base_url}/AlphaSign?msg=<C:RED>Red</C:RED> <C:GREEN>Green</C:GREEN> <C:YELLOW>Yellow</C:YELLOW>&effect=twinkle&speed=3'
        },
        {
            'name': 'Display at Different XY',
            'url': f'{base_url}/display?enabled=true&x=5&y=10&text=Positioned'
        },
        {
            'name': 'Dimming Schedule',
            'url': f'{base_url}/dimming?action=time&start=20&stop=8'
        }
    ]
    
    for test in advanced_tests:
        try:
            response = requests.get(test['url'], timeout=5)
            if response.status_code == 200:
                print(f"[OK] {test['name']}")
            else:
                print(f"[ERROR] {test['name']}: {response.status_code}")
        except Exception as e:
            print(f"[ERROR] {test['name']}: {e}")

def main():
    """Main test function"""
    print("Alpha Sign HTTP Service Test Suite")
    print("=" * 50)
    print("Testing all endpoints for functionality")
    print()
    
    # Test basic endpoints
    success = test_http_endpoints()
    
    # Test advanced features
    test_advanced_features()
    
    print("\n" + "=" * 50)
    if success:
        print("ALL TESTS PASSED!")
        print("The HTTP service is fully functional and ready for use.")
    else:
        print("SOME TESTS FAILED!")
        print("Please review the errors and fix the issues.")
    
    print("\nService is running at: http://localhost:8888")
    print("Try: curl 'http://localhost:8888/help' for usage information")

if __name__ == '__main__':
    main()
