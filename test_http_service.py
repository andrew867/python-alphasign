#!/usr/bin/env python3

"""
Test script for Alpha Sign HTTP Service
Tests all the HTTP endpoints and parameters
"""

import requests
import json
import time
import sys

class AlphaSignHTTPTester:
    """Test the Alpha Sign HTTP service"""
    
    def __init__(self, base_url='http://localhost:8888'):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_basic_message(self):
        """Test basic message sending"""
        print("Testing basic message...")
        try:
            response = self.session.get(f"{self.base_url}/AlphaSign?msg=Hello World")
            if response.status_code == 200:
                print("[OK] Basic message test passed")
                return True
            else:
                print(f"[ERROR] Basic message test failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"[ERROR] Basic message test failed: {e}")
            return False
    
    def test_colors(self):
        """Test different colors"""
        print("Testing colors...")
        colors = ['red', 'green', 'amber', 'yellow', 'orange', 'auto']
        success = True
        
        for color in colors:
            try:
                response = self.session.get(f"{self.base_url}/AlphaSign?msg=Color Test&color={color}")
                if response.status_code != 200:
                    print(f"✗ Color {color} test failed: {response.status_code}")
                    success = False
                else:
                    print(f"✓ Color {color} test passed")
                time.sleep(1)  # Delay between tests
            except Exception as e:
                print(f"✗ Color {color} test failed: {e}")
                success = False
        
        return success
    
    def test_effects(self):
        """Test different effects"""
        print("Testing effects...")
        effects = ['scroll', 'hold', 'flash', 'roll_up', 'roll_down', 'twinkle', 'sparkle', 'auto']
        success = True
        
        for effect in effects:
            try:
                response = self.session.get(f"{self.base_url}/AlphaSign?msg=Effect Test&effect={effect}")
                if response.status_code != 200:
                    print(f"✗ Effect {effect} test failed: {response.status_code}")
                    success = False
                else:
                    print(f"✓ Effect {effect} test passed")
                time.sleep(1)  # Delay between tests
            except Exception as e:
                print(f"✗ Effect {effect} test failed: {e}")
                success = False
        
        return success
    
    def test_speeds(self):
        """Test different speeds"""
        print("Testing speeds...")
        speeds = ['1', '2', '3', '4', '5']
        success = True
        
        for speed in speeds:
            try:
                response = self.session.get(f"{self.base_url}/AlphaSign?msg=Speed Test&speed={speed}")
                if response.status_code != 200:
                    print(f"✗ Speed {speed} test failed: {response.status_code}")
                    success = False
                else:
                    print(f"✓ Speed {speed} test passed")
                time.sleep(1)  # Delay between tests
            except Exception as e:
                print(f"✗ Speed {speed} test failed: {e}")
                success = False
        
        return success
    
    def test_fonts(self):
        """Test different fonts"""
        print("Testing fonts...")
        fonts = ['sans5', 'sans7', 'serif7', 'serif16', 'sans16']
        success = True
        
        for font in fonts:
            try:
                response = self.session.get(f"{self.base_url}/AlphaSign?msg=Font Test&font={font}")
                if response.status_code != 200:
                    print(f"✗ Font {font} test failed: {response.status_code}")
                    success = False
                else:
                    print(f"✓ Font {font} test passed")
                time.sleep(1)  # Delay between tests
            except Exception as e:
                print(f"✗ Font {font} test failed: {e}")
                success = False
        
        return success
    
    def test_lines(self):
        """Test different line positions"""
        print("Testing line positions...")
        lines = ['top', 'middle', 'bottom', 'fill']
        success = True
        
        for line in lines:
            try:
                response = self.session.get(f"{self.base_url}/AlphaSign?msg=Line Test&line={line}")
                if response.status_code != 200:
                    print(f"✗ Line {line} test failed: {response.status_code}")
                    success = False
                else:
                    print(f"✓ Line {line} test passed")
                time.sleep(1)  # Delay between tests
            except Exception as e:
                print(f"✗ Line {line} test failed: {e}")
                success = False
        
        return success
    
    def test_beep(self):
        """Test beep functionality"""
        print("Testing beep...")
        try:
            response = self.session.get(f"{self.base_url}/AlphaSign?msg=Beep Test&beep=3")
            if response.status_code == 200:
                print("✓ Beep test passed")
                return True
            else:
                print(f"✗ Beep test failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Beep test failed: {e}")
            return False
    
    def test_combined_parameters(self):
        """Test combined parameters"""
        print("Testing combined parameters...")
        try:
            response = self.session.get(f"{self.base_url}/AlphaSign?msg=Combined Test&color=red&effect=flash&speed=5&font=sans7&line=top&beep=2")
            if response.status_code == 200:
                print("✓ Combined parameters test passed")
                return True
            else:
                print(f"✗ Combined parameters test failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Combined parameters test failed: {e}")
            return False
    
    def test_status_endpoint(self):
        """Test status endpoint"""
        print("Testing status endpoint...")
        try:
            response = self.session.get(f"{self.base_url}/status")
            if response.status_code == 200:
                data = response.json()
                print("✓ Status endpoint test passed")
                print(f"  Service: {data.get('service', 'Unknown')}")
                print(f"  Version: {data.get('version', 'Unknown')}")
                print(f"  Sign connected: {data.get('sign_connected', False)}")
                return True
            else:
                print(f"✗ Status endpoint test failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Status endpoint test failed: {e}")
            return False
    
    def test_help_endpoint(self):
        """Test help endpoint"""
        print("Testing help endpoint...")
        try:
            response = self.session.get(f"{self.base_url}/help")
            if response.status_code == 200:
                print("✓ Help endpoint test passed")
                return True
            else:
                print(f"✗ Help endpoint test failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Help endpoint test failed: {e}")
            return False
    
    def test_error_handling(self):
        """Test error handling"""
        print("Testing error handling...")
        try:
            # Test missing message parameter
            response = self.session.get(f"{self.base_url}/AlphaSign")
            if response.status_code == 400:
                print("✓ Missing message parameter handled correctly")
            else:
                print(f"✗ Missing message parameter not handled: {response.status_code}")
                return False
            
            # Test invalid endpoint
            response = self.session.get(f"{self.base_url}/invalid")
            if response.status_code == 404:
                print("✓ Invalid endpoint handled correctly")
            else:
                print(f"✗ Invalid endpoint not handled: {response.status_code}")
                return False
            
            return True
        except Exception as e:
            print(f"✗ Error handling test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("Alpha Sign HTTP Service Test Suite")
        print("=" * 40)
        
        tests = [
            ("Basic Message", self.test_basic_message),
            ("Colors", self.test_colors),
            ("Effects", self.test_effects),
            ("Speeds", self.test_speeds),
            ("Fonts", self.test_fonts),
            ("Lines", self.test_lines),
            ("Beep", self.test_beep),
            ("Combined Parameters", self.test_combined_parameters),
            ("Status Endpoint", self.test_status_endpoint),
            ("Help Endpoint", self.test_help_endpoint),
            ("Error Handling", self.test_error_handling),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n{test_name}:")
            if test_func():
                passed += 1
            time.sleep(0.5)  # Small delay between test groups
        
        print("\n" + "=" * 40)
        print(f"Tests passed: {passed}/{total}")
        
        if passed == total:
            print("🎉 All tests passed!")
            return True
        else:
            print("❌ Some tests failed!")
            return False

def main():
    """Main test function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Alpha Sign HTTP Service')
    parser.add_argument('--url', default='http://localhost:8888', help='Service URL')
    parser.add_argument('--quick', action='store_true', help='Run quick tests only')
    
    args = parser.parse_args()
    
    tester = AlphaSignHTTPTester(args.url)
    
    if args.quick:
        # Run only basic tests
        print("Running quick tests...")
        success = (
            tester.test_basic_message() and
            tester.test_status_endpoint() and
            tester.test_help_endpoint()
        )
    else:
        # Run all tests
        success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
