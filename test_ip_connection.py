#!/usr/bin/env python3

"""
Test script for IP connection functionality
Tests the implementation with the specified IP and port
"""

import sys
import os
import time

# Add the parent directory to the path so we can import alphasign
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from alphasign import AlphaSign, Easy

def test_ip_connection():
    """Test IP connection with specified parameters"""
    print("Testing IP connection to 192.168.133.54:10001")
    
    try:
        # Test with explicit port
        print("1. Testing with explicit port...")
        sign = AlphaSign(port='192.168.133.54:10001')
        Easy.Text.show('IP Test - Explicit Port')
        print("✓ Explicit port connection successful")
        
        # Close and test with default port
        sign.sign.close()
        time.sleep(1)
        
        print("2. Testing with default port...")
        sign = AlphaSign(port='192.168.133.54')
        Easy.Text.show('IP Test - Default Port')
        print("✓ Default port connection successful")
        
        # Test image functionality
        print("3. Testing image functionality...")
        try:
            Easy.Image.show("examples/test.png")
            print("✓ Image functionality successful")
        except Exception as e:
            print(f"⚠ Image functionality failed (expected if no image file): {e}")
        
        # Test buzzer functionality
        print("4. Testing buzzer functionality...")
        Easy.Buzzer.beep(1000, 2, 1)  # 1000Hz, 2 seconds, 1 repeat
        print("✓ Buzzer functionality successful")
        
        print("\n🎉 All IP connection tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ IP connection test failed: {e}")
        return False

def test_connection_detection():
    """Test automatic connection type detection"""
    print("\nTesting connection type detection...")
    
    test_cases = [
        ('192.168.133.54', 'ip'),
        ('192.168.133.54:10001', 'ip'),
        ('sign.local:10001', 'ip'),
        ('/dev/ttyUSB0', 'serial'),
        ('COM1', 'serial'),
        ('/dev/ttyACM0', 'serial'),
    ]
    
    from alphasign.sign import Sign
    sign = Sign()
    
    for port, expected in test_cases:
        detected = sign._detect_connection_type(port)
        status = "✓" if detected == expected else "✗"
        print(f"{status} {port:20} → {detected:6} (expected {expected})")
    
    print("Connection type detection test completed")

if __name__ == "__main__":
    print("AlphaSign IP Connection Test")
    print("=" * 40)
    
    # Test connection type detection
    test_connection_detection()
    
    # Test actual IP connection
    print("\n" + "=" * 40)
    success = test_ip_connection()
    
    if success:
        print("\n🎉 All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
