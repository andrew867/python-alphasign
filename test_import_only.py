#!/usr/bin/env python3

"""
Test script to verify that examples can import the library correctly
without actually connecting to hardware
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_import():
    """Test that we can import the library"""
    try:
        from alphasign import AlphaSign, Easy, Sign, Text
        print("[OK] Successfully imported alphasign library")
        return True
    except ImportError as e:
        print(f"[ERROR] Failed to import alphasign: {e}")
        return False

def test_connection_detection():
    """Test connection type detection"""
    try:
        from alphasign.sign import Sign
        sign = Sign()
        
        # Test various port formats
        test_cases = [
            ('192.168.133.54', 'ip'),
            ('192.168.133.54:10001', 'ip'),
            ('/dev/ttyUSB0', 'serial'),
            ('COM1', 'serial'),
        ]
        
        for port, expected in test_cases:
            detected = sign._detect_connection_type(port)
            if detected == expected:
                print(f"[OK] {port} correctly detected as {detected}")
            else:
                print(f"[ERROR] {port} detected as {detected}, expected {expected}")
                return False
        
        return True
    except Exception as e:
        print(f"[ERROR] Connection detection test failed: {e}")
        return False

def test_ip_connection_class():
    """Test IP connection class creation"""
    try:
        from alphasign.ip_connection import IPConnection
        
        # Test creating IP connection (without actually connecting)
        conn = IPConnection('192.168.133.54', 10001)
        print("[OK] IPConnection class created successfully")
        
        # Test parsing
        host, port = conn._parse_ip_connection('192.168.133.54:10001')
        if host == '192.168.133.54' and port == 10001:
            print("[OK] IP connection parsing works correctly")
        else:
            print(f"[ERROR] IP parsing failed: got {host}:{port}")
            return False
            
        return True
    except Exception as e:
        print(f"[ERROR] IP connection test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing AlphaSign Library Import and Setup")
    print("=" * 50)
    
    tests = [
        ("Library Import", test_import),
        ("Connection Detection", test_connection_detection),
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
        print("[SUCCESS] All tests passed!")
        return True
    else:
        print("[WARNING] Some tests failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
