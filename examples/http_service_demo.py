#!/usr/bin/env python3

"""
Demo script for Alpha Sign HTTP Service
Shows how to use the HTTP API to control Alpha signs
"""

import requests
import time
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def demo_basic_usage():
    """Demonstrate basic HTTP service usage"""
    print("Alpha Sign HTTP Service Demo")
    print("=" * 40)
    
    base_url = "http://localhost:8888"
    
    # Test service availability
    try:
        response = requests.get(f"{base_url}/status", timeout=5)
        if response.status_code == 200:
            status = response.json()
            print(f"✓ Service is running (Version: {status.get('version', 'Unknown')})")
            print(f"  Sign connected: {status.get('sign_connected', False)}")
        else:
            print(f"✗ Service status check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Cannot connect to service: {e}")
        print("  Make sure the service is running on localhost:8888")
        return False
    
    print()
    
    # Demo 1: Basic message
    print("Demo 1: Basic Message")
    try:
        response = requests.get(f"{base_url}/AlphaSign?msg=Hello from HTTP!")
        if response.status_code == 200:
            print("✓ Basic message sent successfully")
        else:
            print(f"✗ Basic message failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Basic message error: {e}")
    
    time.sleep(2)
    
    # Demo 2: Colored message
    print("\nDemo 2: Colored Message")
    try:
        response = requests.get(f"{base_url}/AlphaSign?msg=Red Alert&color=red&effect=flash")
        if response.status_code == 200:
            print("✓ Colored message sent successfully")
        else:
            print(f"✗ Colored message failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Colored message error: {e}")
    
    time.sleep(2)
    
    # Demo 3: Speed and effect
    print("\nDemo 3: Speed and Effect")
    try:
        response = requests.get(f"{base_url}/AlphaSign?msg=Fast Message&speed=5&effect=scroll")
        if response.status_code == 200:
            print("✓ Speed/effect message sent successfully")
        else:
            print(f"✗ Speed/effect message failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Speed/effect message error: {e}")
    
    time.sleep(2)
    
    # Demo 4: Font and line
    print("\nDemo 4: Font and Line")
    try:
        response = requests.get(f"{base_url}/AlphaSign?msg=Large Text&font=sans16&line=top")
        if response.status_code == 200:
            print("✓ Font/line message sent successfully")
        else:
            print(f"✗ Font/line message failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Font/line message error: {e}")
    
    time.sleep(2)
    
    # Demo 5: Beep
    print("\nDemo 5: Message with Beep")
    try:
        response = requests.get(f"{base_url}/AlphaSign?msg=Beep Test&beep=3")
        if response.status_code == 200:
            print("✓ Beep message sent successfully")
        else:
            print(f"✗ Beep message failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Beep message error: {e}")
    
    time.sleep(2)
    
    # Demo 6: Combined parameters
    print("\nDemo 6: Combined Parameters")
    try:
        response = requests.get(f"{base_url}/AlphaSign?msg=Welcome&color=green&effect=twinkle&speed=3&font=sans7&line=fill&beep=1")
        if response.status_code == 200:
            print("✓ Combined parameters message sent successfully")
        else:
            print(f"✗ Combined parameters message failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Combined parameters message error: {e}")
    
    print("\n" + "=" * 40)
    print("Demo completed!")
    print("\nTo test manually, try:")
    print("curl 'http://localhost:8888/AlphaSign?msg=Your Message'")
    print("curl 'http://localhost:8888/status'")
    print("curl 'http://localhost:8888/help'")
    
    return True

def demo_advanced_formatting():
    """Demonstrate advanced string formatting"""
    print("\nAdvanced String Formatting Demo")
    print("=" * 40)
    
    base_url = "http://localhost:8888"
    
    # Demo advanced formatting
    advanced_messages = [
        "Welcome to <C:RED>Alpha Sign</C:RED>!",
        "<SPEED:1>Slow <SPEED:5>Fast</SPEED:5></SPEED:1>",
        "<C:GREEN>Green</C:GREEN> <C:RED>Red</C:RED> <C:YELLOW>Yellow</C:YELLOW>",
        "<TWINKLE>Twinkling Text</TWINKLE>",
        "<ANIM:WELCOME>Welcome Animation</ANIM:WELCOME>",
        "Time: <TIME> Date: <DATE>",
        "Line 1\\nLine 2\\nLine 3"
    ]
    
    for i, message in enumerate(advanced_messages, 1):
        print(f"\nDemo {i}: Advanced Formatting")
        print(f"Message: {message}")
        
        try:
            response = requests.get(f"{base_url}/AlphaSign?msg={message}")
            if response.status_code == 200:
                print("✓ Advanced formatting sent successfully")
            else:
                print(f"✗ Advanced formatting failed: {response.status_code}")
        except Exception as e:
            print(f"✗ Advanced formatting error: {e}")
        
        time.sleep(3)  # Longer delay for complex messages
    
    print("\n" + "=" * 40)
    print("Advanced formatting demo completed!")

def main():
    """Main demo function"""
    print("Alpha Sign HTTP Service Demo")
    print("This demo shows how to use the HTTP API to control Alpha signs")
    print()
    
    # Check if requests module is available
    try:
        import requests
    except ImportError:
        print("Error: requests module not found")
        print("Install with: pip install requests")
        return False
    
    # Run basic demo
    if not demo_basic_usage():
        print("\nBasic demo failed. Make sure the service is running.")
        return False
    
    # Ask if user wants to see advanced demo
    try:
        response = input("\nRun advanced formatting demo? (y/n): ").lower()
        if response in ['y', 'yes']:
            demo_advanced_formatting()
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
        return True
    
    print("\nDemo completed successfully!")
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
