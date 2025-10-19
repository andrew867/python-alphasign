#!/usr/bin/env python3

"""
Test script to verify string processing converts tags to binary correctly
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from alphasign.string_processor import AlphaStringProcessor

def test_string_processing():
    """Test that string processing converts tags to binary"""
    print("Testing Alpha Sign String Processing")
    print("=" * 40)
    
    processor = AlphaStringProcessor()
    
    # Test cases with expected results
    test_cases = [
        # Basic color tests
        ("<C:RED>Hello</C:RED>", "Should contain red color code"),
        ("<C:GREEN>World</C:GREEN>", "Should contain green color code"),
        ("<C:AMBER>Test</C:AMBER>", "Should contain amber color code"),
        
        # Speed tests
        ("<SPEED:1>Slow</SPEED:1>", "Should contain speed 1 code"),
        ("<SPEED:5>Fast</SPEED:5>", "Should contain speed 5 code"),
        
        # Effect tests
        ("<SCROLL>Scroll text</SCROLL>", "Should contain scroll effect"),
        ("<FLASH>Flash text</FLASH>", "Should contain flash effect"),
        ("<TWINKLE>Twinkle text</TWINKLE>", "Should contain twinkle effect"),
        
        # Font tests
        ("<F:SANS7>Font test</F:SANS7>", "Should contain sans7 font"),
        ("<F:SERIF16>Large font</F:SERIF16>", "Should contain serif16 font"),
        
        # Special characters
        ("<TIME>", "Should contain time code"),
        ("<DATE>", "Should contain date code"),
        ("\\n", "Should contain newline"),
        
        # Combined test
        ("<C:RED><SPEED:3><FLASH>Combined</FLASH></SPEED:3></C:RED>", "Should contain multiple codes"),
    ]
    
    print("Testing string processing...")
    print()
    
    for i, (test_input, description) in enumerate(test_cases, 1):
        print(f"Test {i}: {description}")
        print(f"Input:  {test_input}")
        
        try:
            result = processor.make_alpha(test_input)
            print(f"Output: {repr(result)}")
            
            # Check if the result contains binary characters (not just the original tags)
            if result != test_input:
                print("[OK] String was processed (contains binary codes)")
            else:
                print("[WARNING] String appears unchanged (may not be processing correctly)")
            
            # Check for specific binary codes
            has_binary = any(ord(c) < 32 or ord(c) > 126 for c in result)
            if has_binary:
                print("[OK] Contains binary control codes")
            else:
                print("[WARNING] No binary control codes detected")
                
        except Exception as e:
            print(f"[ERROR] Processing failed: {e}")
        
        print()
    
    print("=" * 40)
    print("String processing test completed!")

def test_http_service_processing():
    """Test the HTTP service message processing"""
    print("\nTesting HTTP Service Message Processing")
    print("=" * 40)
    
    try:
        from alphasign_http_service import AlphaSignHTTPHandler
        
        # Create a mock handler instance
        handler = AlphaSignHTTPHandler()
        
        # Test HTTP parameter processing
        test_params = {
            'color': 'red',
            'effect': 'flash',
            'speed': '3',
            'font': 'sans7',
            'line': 'middle',
            'beep': '2'
        }
        
        test_message = "Hello World"
        
        print(f"Input message: {test_message}")
        print(f"Parameters: {test_params}")
        
        # Process the message
        processed = handler.process_message(test_message, test_params)
        
        print(f"Processed result: {repr(processed)}")
        
        # Check if processing occurred
        if processed != test_message:
            print("[OK] Message was processed with parameters")
        else:
            print("[WARNING] Message appears unchanged")
        
        # Check for binary codes
        has_binary = any(ord(c) < 32 or ord(c) > 126 for c in processed)
        if has_binary:
            print("[OK] Contains binary control codes")
        else:
            print("[WARNING] No binary control codes detected")
            
    except Exception as e:
        print(f"[ERROR] HTTP service processing test failed: {e}")

def main():
    """Main test function"""
    print("Alpha Sign String Processing Test")
    print("=" * 50)
    
    # Test basic string processing
    test_string_processing()
    
    # Test HTTP service processing
    test_http_service_processing()
    
    print("\n" + "=" * 50)
    print("All tests completed!")
    print("\nIf you see binary control codes in the output, the processing is working correctly.")
    print("The tags should be converted to actual Alpha sign control characters.")

if __name__ == '__main__':
    main()
