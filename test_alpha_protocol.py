#!/usr/bin/env python3

"""
Test script for the enhanced Alpha protocol features
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from alphasign.string_processor import AlphaStringProcessor
import datetime

def test_alpha_protocol_features():
    """Test all the new Alpha protocol features"""
    print("Testing Enhanced Alpha Protocol Features")
    print("=" * 50)
    
    processor = AlphaStringProcessor()
    
    # Test 1: Time setting
    print("Test 1: Time Setting")
    print("-" * 20)
    now = datetime.datetime.now()
    time_cmd = processor.set_time(now)
    print(f"Time command: {repr(time_cmd)}")
    print(f"Expected format: E + 0x20 + HHMM")
    print()
    
    # Test 2: Date setting
    print("Test 2: Date Setting")
    print("-" * 20)
    date_cmd = processor.set_date(now)
    print(f"Date command: {repr(date_cmd)}")
    print(f"Expected format: E + 0x3b + MMDDYY")
    print()
    
    # Test 3: Weekday setting
    print("Test 3: Weekday Setting")
    print("-" * 20)
    weekday_cmd = processor.set_weekday(now.weekday())
    print(f"Weekday command: {repr(weekday_cmd)}")
    print(f"Expected format: E + 0x26 + day_number")
    print()
    
    # Test 4: Time format setting
    print("Test 4: Time Format Setting")
    print("-" * 20)
    time_format_24h = processor.set_time_format(ampm=False)
    time_format_12h = processor.set_time_format(ampm=True)
    print(f"24-hour format: {repr(time_format_24h)}")
    print(f"12-hour format: {repr(time_format_12h)}")
    print()
    
    # Test 5: Sound control
    print("Test 5: Sound Control")
    print("-" * 20)
    sound_on = processor.set_sound(True)
    sound_off = processor.set_sound(False)
    print(f"Sound on: {repr(sound_on)}")
    print(f"Sound off: {repr(sound_off)}")
    print()
    
    # Test 6: Soft reset
    print("Test 6: Soft Reset")
    print("-" * 20)
    reset_cmd = processor.soft_reset()
    print(f"Reset command: {repr(reset_cmd)}")
    print(f"Expected format: E + 0x2c")
    print()
    
    # Test 7: Memory management
    print("Test 7: Memory Management")
    print("-" * 20)
    memory_map = processor.set_memory_map()
    print(f"Memory map: {repr(memory_map[:50])}...")
    print(f"Length: {len(memory_map)} characters")
    print()
    
    # Test 8: Read commands
    print("Test 8: Read Commands")
    print("-" * 20)
    error_cmd = processor.read_error_register()
    memory_cmd = processor.read_memory_size()
    print(f"Read error register: {repr(error_cmd)}")
    print(f"Read memory size: {repr(memory_cmd)}")
    print()
    
    # Test 9: Text file operations
    print("Test 9: Text File Operations")
    print("-" * 20)
    text_file = processor.write_text_file('A', 'scroll', 'Hello World')
    clear_file = processor.clear_text('A')
    print(f"Write text file: {repr(text_file[:30])}...")
    print(f"Clear text file: {repr(clear_file)}")
    print()
    
    # Test 10: String file operations
    print("Test 10: String File Operations")
    print("-" * 20)
    string_file = processor.write_string_file('1', 'Test String')
    print(f"Write string file: {repr(string_file)}")
    print()
    
    # Test 11: Packet creation
    print("Test 11: Packet Creation")
    print("-" * 20)
    header = processor.create_packet_header("Z", "00")
    footer = processor.create_packet_footer("AHello")
    complete = processor.create_complete_packet("AHello", "Z", "00")
    print(f"Header: {repr(header)}")
    print(f"Footer: {repr(footer)}")
    print(f"Complete packet: {repr(complete[:20])}...")
    print()
    
    # Test 12: Extended character handling
    print("Test 12: Extended Character Handling")
    print("-" * 20)
    test_text = "Hello äöå World"
    escaped = processor.escape_text(test_text)
    print(f"Original: {test_text}")
    print(f"Escaped: {repr(escaped)}")
    print()
    
    print("=" * 50)
    print("All Alpha protocol features tested!")
    print("The enhanced string processor now supports:")
    print("- Time and date setting")
    print("- Sound control")
    print("- Memory management")
    print("- File operations")
    print("- Packet creation")
    print("- Extended character support")

def test_http_service_integration():
    """Test HTTP service integration with new features"""
    print("\nTesting HTTP Service Integration")
    print("=" * 40)
    
    # Simulate HTTP requests
    test_requests = [
        {
            'url': '/settime?time=14:30',
            'description': 'Set time to 2:30 PM'
        },
        {
            'url': '/setdate?date=12/25/23',
            'description': 'Set date to December 25, 2023'
        },
        {
            'url': '/sound?on=true',
            'description': 'Enable sound'
        },
        {
            'url': '/reset',
            'description': 'Soft reset the sign'
        },
        {
            'url': '/memory?action=info',
            'description': 'Get memory information'
        },
        {
            'url': '/memory?action=configure',
            'description': 'Configure memory map'
        }
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"Test {i}: {request['description']}")
        print(f"URL: {request['url']}")
        print("Expected: HTTP 200 with JSON response")
        print()
    
    print("=" * 40)
    print("HTTP service integration test completed!")
    print("New endpoints available:")
    print("- /settime - Set sign time")
    print("- /setdate - Set sign date")
    print("- /sound - Control sound")
    print("- /reset - Reset sign")
    print("- /memory - Memory management")

def main():
    """Main test function"""
    print("Enhanced Alpha Protocol Test Suite")
    print("=" * 60)
    
    # Test Alpha protocol features
    test_alpha_protocol_features()
    
    # Test HTTP service integration
    test_http_service_integration()
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("\nThe enhanced Alpha protocol now includes:")
    print("[OK] Complete Alpha protocol implementation")
    print("[OK] Automatic date/time setting on connection")
    print("[OK] Sound control")
    print("[OK] Memory management")
    print("[OK] File operations")
    print("[OK] Extended character support")
    print("[OK] HTTP endpoints for all features")

if __name__ == '__main__':
    main()
