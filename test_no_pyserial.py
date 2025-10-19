#!/usr/bin/env python3

"""
Test script to verify functionality without pyserial installed
This simulates the behavior when pyserial is not available
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_import_without_pyserial():
    """Test that we can import the library even without pyserial"""
    try:
        # Temporarily remove pyserial from sys.modules if it exists
        if 'serial' in sys.modules:
            del sys.modules['serial']
        
        from alphasign import AlphaSign, Easy, Sign, Text
        print("[OK] Successfully imported alphasign library")
        return True
    except ImportError as e:
        print(f"[ERROR] Failed to import alphasign: {e}")
        return False

def test_connection_availability():
    """Test connection availability detection"""
    try:
        from alphasign.sign import Sign
        
        # Check available connections
        available = Sign.get_available_connections()
        print(f"[INFO] Available connections: {available}")
        
        # Check if serial is available
        serial_available = Sign.is_serial_available()
        print(f"[INFO] Serial available: {serial_available}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Connection availability test failed: {e}")
        return False

def test_ip_only_functionality():
    """Test that IP functionality works without pyserial"""
    try:
        from alphasign import Sign
        
        sign = Sign()
        
        # Test IP connection detection
        ip_type = sign._detect_connection_type('192.168.133.54:10001')
        if ip_type == 'ip':
            print("[OK] IP connection type correctly detected")
        else:
            print(f"[ERROR] Expected 'ip', got '{ip_type}'")
            return False
        
        # Test IP connection parsing
        host, port = sign._parse_ip_connection('192.168.133.54:10001')
        if host == '192.168.133.54' and port == 10001:
            print("[OK] IP connection parsing works")
        else:
            print(f"[ERROR] IP parsing failed: got {host}:{port}")
            return False
        
        return True
    except Exception as e:
        print(f"[ERROR] IP functionality test failed: {e}")
        return False

def test_serial_error_handling():
    """Test that serial connections fail gracefully without pyserial"""
    try:
        from alphasign import Sign
        
        sign = Sign()
        
        # This should raise an ImportError
        try:
            sign.open(port='/dev/ttyUSB0')
            print("[ERROR] Serial connection should have failed")
            return False
        except ImportError as e:
            if "pyserial is not installed" in str(e):
                print("[OK] Serial connection properly fails with helpful error")
                return True
            else:
                print(f"[ERROR] Unexpected error: {e}")
                return False
        except Exception as e:
            print(f"[ERROR] Unexpected exception type: {e}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Serial error handling test failed: {e}")
        return False

def test_ip_connection_class():
    """Test IP connection class works without pyserial"""
    try:
        from alphasign.ip_connection import IPConnection
        
        # Test creating IP connection (without actually connecting)
        conn = IPConnection('192.168.133.54', 10001)
        print("[OK] IPConnection class works without pyserial")
        
        return True
    except Exception as e:
        print(f"[ERROR] IP connection class test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing AlphaSign Library Without pyserial")
    print("=" * 50)
    
    tests = [
        ("Library Import", test_import_without_pyserial),
        ("Connection Availability", test_connection_availability),
        ("IP Functionality", test_ip_only_functionality),
        ("Serial Error Handling", test_serial_error_handling),
        ("IP Connection Class", test_ip_connection_class),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        if test_func():
            passed += 1
            print(f"[SUCCESS] {test_name} passed")
        else:
            print(f"[FAILED] {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("[SUCCESS] All tests passed! Library works without pyserial.")
        return True
    else:
        print("[WARNING] Some tests failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
