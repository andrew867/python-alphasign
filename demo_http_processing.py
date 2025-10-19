#!/usr/bin/env python3

"""
Demo script showing how the HTTP service processes messages
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from alphasign.string_processor import AlphaStringProcessor

def demo_http_requests():
    """Demonstrate how HTTP requests would be processed"""
    print("Alpha Sign HTTP Service - Message Processing Demo")
    print("=" * 60)
    
    processor = AlphaStringProcessor()
    
    # Simulate HTTP request processing
    def simulate_http_request(url_params):
        """Simulate processing an HTTP request"""
        # Extract parameters (like the HTTP service does)
        params = {
            'msg': url_params.get('msg', [''])[0],
            'color': url_params.get('color', ['auto'])[0],
            'effect': url_params.get('effect', ['scroll'])[0],
            'speed': url_params.get('speed', ['3'])[0],
            'font': url_params.get('font', ['sans7'])[0],
            'line': url_params.get('line', ['middle'])[0],
            'beep': url_params.get('beep', ['0'])[0],
            'label': url_params.get('label', ['A'])[0]
        }
        
        if not params['msg']:
            return "Error: Missing 'msg' parameter"
        
        # Process the message (like the HTTP service does)
        processed = params['msg']
        
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
        
        # Convert to binary (this is the key step!)
        binary_result = processor.make_alpha(processed)
        
        return {
            'original': params['msg'],
            'processed_tags': processed,
            'binary_result': binary_result,
            'params_used': params
        }
    
    # Demo HTTP requests
    demo_requests = [
        {
            'url': '/AlphaSign?msg=Hello World',
            'params': {'msg': ['Hello World']},
            'description': 'Basic message'
        },
        {
            'url': '/AlphaSign?msg=Welcome&color=red&effect=flash&speed=5',
            'params': {'msg': ['Welcome'], 'color': ['red'], 'effect': ['flash'], 'speed': ['5']},
            'description': 'Red flash message'
        },
        {
            'url': '/AlphaSign?msg=Alert&color=amber&effect=twinkle&beep=3',
            'params': {'msg': ['Alert'], 'color': ['amber'], 'effect': ['twinkle'], 'beep': ['3']},
            'description': 'Amber twinkle alert with beep'
        },
        {
            'url': '/AlphaSign?msg=Welcome&color=green&effect=scroll&speed=1&font=sans16',
            'params': {'msg': ['Welcome'], 'color': ['green'], 'effect': ['scroll'], 'speed': ['1'], 'font': ['sans16']},
            'description': 'Green slow scroll with large font'
        },
        {
            'url': '/AlphaSign?msg=<C:RED>Red</C:RED> <C:GREEN>Green</C:GREEN> <C:YELLOW>Yellow</C:YELLOW>',
            'params': {'msg': ['<C:RED>Red</C:RED> <C:GREEN>Green</C:GREEN> <C:YELLOW>Yellow</C:YELLOW>']},
            'description': 'Message with embedded color tags'
        }
    ]
    
    for i, request in enumerate(demo_requests, 1):
        print(f"Demo {i}: {request['description']}")
        print(f"URL: {request['url']}")
        
        try:
            result = simulate_http_request(request['params'])
            
            if isinstance(result, dict):
                print(f"Original message: {result['original']}")
                print(f"Processed tags: {result['processed_tags']}")
                print(f"Binary result: {repr(result['binary_result'])}")
                print(f"Parameters used: {result['params_used']}")
                
                # Check if binary conversion worked
                has_binary = any(ord(c) < 32 or ord(c) > 126 for c in result['binary_result'])
                if has_binary:
                    print("[OK] Successfully converted to binary control codes")
                else:
                    print("[WARNING] No binary control codes detected")
            else:
                print(f"Error: {result}")
                
        except Exception as e:
            print(f"[ERROR] Processing failed: {e}")
        
        print("-" * 60)
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("\nThe HTTP service now properly converts tags to binary control codes.")
    print("When you send a request like:")
    print("  curl 'http://localhost:8888/AlphaSign?msg=Hello&color=red&effect=flash'")
    print("The service will convert the parameters to binary Alpha sign commands.")

def main():
    """Main demo function"""
    demo_http_requests()

if __name__ == '__main__':
    main()
