#!/usr/bin/env python3

"""
Demo script showing IP-only functionality without pyserial dependency
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphasign import AlphaSign, Easy, Sign

def demo_connection_availability():
    """Show what connection types are available"""
    print("Connection Availability Demo")
    print("=" * 30)
    
    # Check available connections
    available = Sign.get_available_connections()
    print(f"Available connections: {available}")
    
    # Check if serial is available
    serial_available = Sign.is_serial_available()
    print(f"Serial available: {serial_available}")
    
    if not serial_available:
        print("Note: pyserial not installed - only IP connections available")
    print()

def demo_ip_connection():
    """Demo IP connection functionality"""
    print("IP Connection Demo")
    print("=" * 20)
    
    try:
        # This will work even without pyserial
        sign = AlphaSign(port='192.168.133.54:10001')
        print("[OK] IP connection created successfully")
        
        # Show text
        Easy.Text.show('Hello from IP!')
        print("[OK] Text sent via IP connection")
        
        return True
    except Exception as e:
        print(f"[ERROR] IP connection failed: {e}")
        return False

def demo_serial_error_handling():
    """Demo how serial connections fail gracefully"""
    print("Serial Error Handling Demo")
    print("=" * 30)
    
    try:
        # This should fail with a helpful error
        sign = AlphaSign(port='/dev/ttyUSB0')
        print("[ERROR] Serial connection should have failed")
        return False
    except ImportError as e:
        if "pyserial is not installed" in str(e):
            print("[OK] Serial connection properly fails with helpful error")
            print(f"  Error message: {e}")
            return True
        else:
            print(f"[ERROR] Unexpected error: {e}")
            return False
    except Exception as e:
        print(f"[ERROR] Unexpected exception: {e}")
        return False

def main():
    """Run the IP-only demo"""
    print("AlphaSign IP-Only Functionality Demo")
    print("=" * 40)
    print("This demo shows how the library works with IP connections")
    print("without requiring pyserial for serial connections.")
    print()
    
    # Demo connection availability
    demo_connection_availability()
    
    # Demo IP functionality
    print("Testing IP connection...")
    ip_success = demo_ip_connection()
    print()
    
    # Demo serial error handling
    print("Testing serial error handling...")
    serial_error_success = demo_serial_error_handling()
    print()
    
    # Summary
    print("=" * 40)
    if ip_success and serial_error_success:
        print("[SUCCESS] All demos successful!")
        print("The library works perfectly for IP-only usage.")
    else:
        print("[WARNING] Some demos failed")
    
    print("\nTo use serial connections, install pyserial:")
    print("pip install pyserial")

if __name__ == "__main__":
    main()
