#!/usr/bin/env python3

"""
Example demonstrating both serial and IP connections
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphasign import AlphaSign, Easy

def demo_serial_connection():
    """Demo using traditional serial connection"""
    print("Demo: Serial Connection")
    try:
        # Traditional serial connection
        sign = AlphaSign(port='/dev/ttyUSB0')  # or 'COM1' on Windows
        Easy.Text.show('Serial Connection Test')
        print("✓ Serial connection successful")
    except Exception as e:
        print(f"✗ Serial connection failed: {e}")

def demo_ip_connection():
    """Demo using IP connection"""
    print("Demo: IP Connection")
    try:
        # IP connection with explicit port
        sign = AlphaSign(port='192.168.133.54:10001')
        Easy.Text.show('IP Connection Test')
        print("✓ IP connection successful")
    except Exception as e:
        print(f"✗ IP connection failed: {e}")

def demo_ip_default_port():
    """Demo using IP connection with default port"""
    print("Demo: IP Connection (Default Port)")
    try:
        # IP connection using default port 10001
        sign = AlphaSign(port='192.168.133.54')
        Easy.Text.show('IP Default Port Test')
        print("✓ IP connection (default port) successful")
    except Exception as e:
        print(f"✗ IP connection (default port) failed: {e}")

if __name__ == "__main__":
    print("AlphaSign Connection Demo")
    print("=" * 40)
    
    # Demo different connection types
    demo_serial_connection()
    print()
    demo_ip_connection()
    print()
    demo_ip_default_port()
