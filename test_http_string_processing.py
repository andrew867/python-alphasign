#!/usr/bin/env python3

"""
Test HTTP service string processing without creating a full HTTP handler
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from alphasign.string_processor import AlphaStringProcessor

def test_http_parameter_processing():
    """Test HTTP parameter processing like the HTTP service does"""
    print("Testing HTTP Parameter Processing")
    print("=" * 40)
    
    processor = AlphaStringProcessor()
    
    # Simulate HTTP parameter processing
    def process_message(message, params):
        """Simulate the HTTP service process_message method"""
        processed = message
        
        # Add color formatting
        color_map = {
            'red': '<C:RED>',
            'green': '<C:GREEN>',
            'amber': '<C:AMBER>',
            'yellow': '<C:YELLOW>',
            'orange': '<C:ORANGE>',
            'auto': '<C:AUTO>',
            'rain1': '<C:RAIN1>',
            'rain2': '<C:RAIN2>',
            'mix': '<C:COLORMIX>'
        }
        
        if params['color'] in color_map:
            processed = color_map[params['color']] + processed
        
        # Add speed formatting
        speed_map = {
            '1': '<SPEED:1>',
            '2': '<SPEED:2>',
            '3': '<SPEED:3>',
            '4': '<SPEED:4>',
            '5': '<SPEED:5>'
        }
        
        if params['speed'] in speed_map:
            processed = speed_map[params['speed']] + processed
        
        # Add effect formatting
        effect_map = {
            'scroll': '<SCROLL>',
            'hold': '<HOLD>',
            'flash': '<FLASH>',
            'roll_up': '<ROLL:UP>',
            'roll_down': '<ROLL:DOWN>',
            'roll_left': '<ROLL:LEFT>',
            'roll_right': '<ROLL:RIGHT>',
            'wipe_up': '<WIPE:UP>',
            'wipe_down': '<WIPE:DOWN>',
            'wipe_left': '<WIPE:LEFT>',
            'wipe_right': '<WIPE:RIGHT>',
            'twinkle': '<TWINKLE>',
            'sparkle': '<SPARKLE>',
            'snow': '<SNOW>',
            'auto': '<AUTO>'
        }
        
        if params['effect'] in effect_map:
            processed = effect_map[params['effect']] + processed
        
        # Add beep if requested
        if params['beep'] != '0':
            try:
                beep_count = int(params['beep'])
                if beep_count > 0:
                    processed += f'<BEEP:{beep_count}>'
            except ValueError:
                pass
        
        # Process through the string processor to convert tags to binary
        return processor.make_alpha(processed)
    
    # Test cases
    test_cases = [
        {
            'message': 'Hello World',
            'params': {'color': 'red', 'effect': 'flash', 'speed': '3', 'beep': '0'},
            'description': 'Red flash message'
        },
        {
            'message': 'Welcome',
            'params': {'color': 'green', 'effect': 'scroll', 'speed': '5', 'beep': '2'},
            'description': 'Green scroll with beep'
        },
        {
            'message': 'Alert',
            'params': {'color': 'amber', 'effect': 'twinkle', 'speed': '1', 'beep': '3'},
            'description': 'Amber twinkle alert'
        },
        {
            'message': 'Test Message',
            'params': {'color': 'auto', 'effect': 'auto', 'speed': '3', 'beep': '0'},
            'description': 'Auto color and effect'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['description']}")
        print(f"Message: {test_case['message']}")
        print(f"Params: {test_case['params']}")
        
        try:
            result = process_message(test_case['message'], test_case['params'])
            print(f"Result: {repr(result)}")
            
            # Check if processing occurred
            if result != test_case['message']:
                print("[OK] Message was processed")
            else:
                print("[WARNING] Message appears unchanged")
            
            # Check for binary codes
            has_binary = any(ord(c) < 32 or ord(c) > 126 for c in result)
            if has_binary:
                print("[OK] Contains binary control codes")
            else:
                print("[WARNING] No binary control codes detected")
                
        except Exception as e:
            print(f"[ERROR] Processing failed: {e}")
        
        print()
    
    print("=" * 40)
    print("HTTP parameter processing test completed!")

def test_direct_string_processing():
    """Test direct string processing with tags"""
    print("\nTesting Direct String Processing")
    print("=" * 40)
    
    processor = AlphaStringProcessor()
    
    # Test cases with opening and closing tags
    test_cases = [
        ("<C:RED>Hello</C:RED>", "Red text with closing tag"),
        ("<SPEED:3>Fast</SPEED:3>", "Speed with closing tag"),
        ("<C:GREEN><SPEED:1>Slow Green</SPEED:1></C:GREEN>", "Combined with closing tags"),
        ("<FLASH>Flash text</FLASH>", "Effect with closing tag"),
    ]
    
    for i, (test_input, description) in enumerate(test_cases, 1):
        print(f"Test {i}: {description}")
        print(f"Input:  {test_input}")
        
        try:
            result = processor.make_alpha(test_input)
            print(f"Output: {repr(result)}")
            
            # Check if processing occurred
            if result != test_input:
                print("[OK] String was processed")
            else:
                print("[WARNING] String appears unchanged")
            
            # Check for binary codes
            has_binary = any(ord(c) < 32 or ord(c) > 126 for c in result)
            if has_binary:
                print("[OK] Contains binary control codes")
            else:
                print("[WARNING] No binary control codes detected")
                
        except Exception as e:
            print(f"[ERROR] Processing failed: {e}")
        
        print()

def main():
    """Main test function"""
    print("HTTP Service String Processing Test")
    print("=" * 50)
    
    # Test HTTP parameter processing
    test_http_parameter_processing()
    
    # Test direct string processing
    test_direct_string_processing()
    
    print("\n" + "=" * 50)
    print("All tests completed!")
    print("\nThe string processing should convert HTML-like tags to binary control codes.")
    print("If you see binary characters (like \\x1c, \\x15, etc.), the processing is working correctly.")

if __name__ == '__main__':
    main()
