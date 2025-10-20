#!/usr/bin/env python3

"""
Demo script showing the enhanced Alpha protocol features
"""

import sys
import os
import datetime

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from alphasign.string_processor import AlphaStringProcessor

def demo_alpha_protocol_features():
    """Demonstrate all the new Alpha protocol features"""
    print("Enhanced Alpha Protocol Features Demo")
    print("=" * 50)
    
    processor = AlphaStringProcessor()
    
    print("1. Time and Date Management")
    print("-" * 30)
    now = datetime.datetime.now()
    
    # Set current time
    time_cmd = processor.set_time(now)
    print(f"Set time command: {repr(time_cmd)}")
    print(f"Sets sign time to: {now.strftime('%H:%M')}")
    
    # Set current date
    date_cmd = processor.set_date(now)
    print(f"Set date command: {repr(date_cmd)}")
    print(f"Sets sign date to: {now.strftime('%m/%d/%y')}")
    
    # Set weekday
    weekday_cmd = processor.set_weekday(now.weekday())
    print(f"Set weekday command: {repr(weekday_cmd)}")
    print(f"Sets weekday to: {now.strftime('%A')}")
    
    print()
    
    print("2. Sound Control")
    print("-" * 20)
    sound_on = processor.set_sound(True)
    sound_off = processor.set_sound(False)
    print(f"Enable sound: {repr(sound_on)}")
    print(f"Disable sound: {repr(sound_off)}")
    print()
    
    print("3. Memory Management")
    print("-" * 25)
    memory_map = processor.set_memory_map()
    print(f"Memory map command: {repr(memory_map[:50])}...")
    print("Creates 5 text files (A-E) and 10 string files (1-10)")
    
    # Read memory info
    memory_info = processor.read_memory_size()
    print(f"Read memory size: {repr(memory_info)}")
    print()
    
    print("4. File Operations")
    print("-" * 20)
    
    # Write text file
    text_file = processor.write_text_file('A', 'scroll', 'Hello World')
    print(f"Write text file: {repr(text_file)}")
    
    # Write string file
    string_file = processor.write_string_file('1', 'Test String')
    print(f"Write string file: {repr(string_file)}")
    
    # Clear text file
    clear_file = processor.clear_text('A')
    print(f"Clear text file: {repr(clear_file)}")
    print()
    
    print("5. Sign Control")
    print("-" * 20)
    
    # Soft reset
    reset_cmd = processor.soft_reset()
    print(f"Soft reset: {repr(reset_cmd)}")
    
    # Time format
    time_format_24h = processor.set_time_format(ampm=False)
    time_format_12h = processor.set_time_format(ampm=True)
    print(f"24-hour format: {repr(time_format_24h)}")
    print(f"12-hour format: {repr(time_format_12h)}")
    print()
    
    print("6. Packet Creation")
    print("-" * 20)
    
    # Create complete packet
    packet = processor.create_complete_packet("AHello World", "Z", "00")
    print(f"Complete packet: {repr(packet[:30])}...")
    print("Includes header, data, checksum, and footer")
    print()
    
    print("7. Extended Character Support")
    print("-" * 30)
    
    # Test extended characters
    test_text = "Hello äöå World"
    escaped = processor.escape_text(test_text)
    print(f"Original text: {test_text}")
    print(f"Escaped text: {repr(escaped)}")
    print("Supports Nordic characters: ä, ö, å, Ä, Ö, Å")
    print()

def demo_http_endpoints():
    """Demonstrate the new HTTP endpoints"""
    print("New HTTP Endpoints Demo")
    print("=" * 30)
    
    endpoints = [
        {
            'url': '/settime?time=14:30',
            'description': 'Set sign time to 2:30 PM',
            'method': 'GET'
        },
        {
            'url': '/setdate?date=12/25/23',
            'description': 'Set sign date to December 25, 2023',
            'method': 'GET'
        },
        {
            'url': '/sound?on=true',
            'description': 'Enable sign sound',
            'method': 'GET'
        },
        {
            'url': '/sound?on=false',
            'description': 'Disable sign sound',
            'method': 'GET'
        },
        {
            'url': '/reset',
            'description': 'Soft reset the sign',
            'method': 'GET'
        },
        {
            'url': '/memory?action=info',
            'description': 'Get memory information',
            'method': 'GET'
        },
        {
            'url': '/memory?action=configure',
            'description': 'Configure memory map',
            'method': 'GET'
        }
    ]
    
    for i, endpoint in enumerate(endpoints, 1):
        print(f"{i}. {endpoint['method']} {endpoint['url']}")
        print(f"   {endpoint['description']}")
        print()
    
    print("All endpoints return JSON responses with status information")

def demo_automatic_datetime():
    """Demonstrate automatic date/time setting"""
    print("Automatic Date/Time Setting Demo")
    print("=" * 35)
    
    print("When the HTTP service connects to the sign, it automatically:")
    print("1. Sets the current time")
    print("2. Sets the current date")
    print("3. Sets the current weekday")
    print("4. Sets 24-hour time format")
    print()
    
    print("This ensures the sign's internal clock is synchronized")
    print("with the server's system time.")
    print()
    
    print("Manual time/date setting is also available via HTTP endpoints:")
    print("- /settime?time=14:30")
    print("- /setdate?date=12/25/23")
    print()

def demo_usage_examples():
    """Show practical usage examples"""
    print("Usage Examples")
    print("=" * 20)
    
    print("1. Basic Message with Auto Date/Time")
    print("   curl 'http://localhost:8888/AlphaSign?msg=Hello World'")
    print("   (Automatically sets date/time on first connection)")
    print()
    
    print("2. Set Custom Time")
    print("   curl 'http://localhost:8888/settime?time=14:30'")
    print("   Response: {\"status\": \"success\", \"time\": \"14:30\"}")
    print()
    
    print("3. Enable Sound")
    print("   curl 'http://localhost:8888/sound?on=true'")
    print("   Response: {\"status\": \"success\", \"sound_on\": true}")
    print()
    
    print("4. Reset Sign")
    print("   curl 'http://localhost:8888/reset'")
    print("   Response: {\"status\": \"success\", \"message\": \"Sign reset successfully\"}")
    print()
    
    print("5. Configure Memory")
    print("   curl 'http://localhost:8888/memory?action=configure'")
    print("   Response: {\"status\": \"success\", \"message\": \"Memory map configured\"}")
    print()

def main():
    """Main demo function"""
    print("Enhanced Alpha Protocol Demo")
    print("=" * 60)
    print()
    
    # Demo Alpha protocol features
    demo_alpha_protocol_features()
    
    # Demo HTTP endpoints
    demo_http_endpoints()
    
    # Demo automatic date/time setting
    demo_automatic_datetime()
    
    # Demo usage examples
    demo_usage_examples()
    
    print("=" * 60)
    print("Enhanced Alpha Protocol Demo Complete!")
    print()
    print("The enhanced library now provides:")
    print("[OK] Complete Alpha protocol implementation")
    print("[OK] Automatic date/time synchronization")
    print("[OK] Sound control")
    print("[OK] Memory management")
    print("[OK] File operations")
    print("[OK] Extended character support")
    print("[OK] HTTP endpoints for all features")
    print()
    print("Ready for production use with full Alpha sign control!")

if __name__ == '__main__':
    main()
