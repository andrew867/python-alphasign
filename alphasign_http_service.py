#!/usr/bin/env python3

"""
Alpha Sign HTTP Service
A systemd-compatible HTTP service for controlling Alpha signs via HTTP requests.
"""

import sys
import os
import json
import time
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from alphasign import AlphaSign, Easy, Sign
from alphasign.string_processor import AlphaStringProcessor

class AlphaSignHTTPHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Alpha Sign service"""
    
    def __init__(self, *args, **kwargs):
        self.sign_connection = None
        self.string_processor = AlphaStringProcessor()
        super().__init__(*args, **kwargs)
    
    def log_message(self, format, *args):
        """Override to use our logging system"""
        logging.info(f"{self.address_string()} - {format % args}")
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            query_params = parse_qs(parsed_url.query)
            
            if path == '/AlphaSign':
                self.handle_alpha_sign_request(query_params)
            elif path == '/status':
                self.handle_status_request()
            elif path == '/help':
                self.handle_help_request()
            else:
                self.send_error(404, "Not Found")
                
        except Exception as e:
            logging.error(f"Error handling request: {e}")
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def handle_alpha_sign_request(self, params):
        """Handle the main AlphaSign request"""
        try:
            # Extract parameters
            message = params.get('msg', [''])[0]
            color = params.get('color', ['auto'])[0]
            effect = params.get('effect', ['scroll'])[0]
            speed = params.get('speed', ['3'])[0]
            font = params.get('font', ['sans7'])[0]
            line = params.get('line', ['middle'])[0]
            beep = params.get('beep', ['0'])[0]
            label = params.get('label', ['A'])[0]
            
            if not message:
                self.send_error(400, "Missing 'msg' parameter")
                return
            
            # Process the message
            processed_message = self.process_message(message, {
                'color': color,
                'effect': effect,
                'speed': speed,
                'font': font,
                'line': line,
                'beep': beep,
                'label': label
            })
            
            # Send to sign
            if self.send_to_sign(processed_message, label):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'status': 'success',
                    'message': 'Text sent to Alpha sign',
                    'original': message,
                    'processed': processed_message
                }
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_error(500, "Failed to send to Alpha sign")
                
        except Exception as e:
            logging.error(f"Error processing AlphaSign request: {e}")
            self.send_error(500, f"Error: {str(e)}")
    
    def process_message(self, message, params):
        """Process the message with Alpha sign formatting"""
        # Start with the basic message
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
        
        # Add font formatting
        font_map = {
            'sans5': '<F:SANS5>',
            'sans7': '<F:SANS7>',
            'serif7': '<F:SERIF7>',
            'serif16': '<F:SERIF16>',
            'sans16': '<F:SANS16>'
        }
        
        if params['font'] in font_map:
            processed = font_map[params['font']] + processed
        
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
        
        # Add line positioning
        line_map = {
            'top': '<LINE:TOP>',
            'middle': '<LINE:MIDDLE>',
            'bottom': '<LINE:BOTTOM>',
            'fill': '<LINE:FILL>'
        }
        
        if params['line'] in line_map:
            processed = line_map[params['line']] + processed
        
        # Add beep if requested
        if params['beep'] != '0':
            try:
                beep_count = int(params['beep'])
                if beep_count > 0:
                    processed += f'<BEEP:{beep_count}>'
            except ValueError:
                pass
        
        # Process through the string processor to convert tags to binary
        return self.string_processor.make_alpha(processed)
    
    def send_to_sign(self, message, label='A'):
        """Send message to the Alpha sign"""
        try:
            if not self.sign_connection:
                # Initialize connection
                self.sign_connection = AlphaSign(port='192.168.133.54:10001')
            
            # Send the text
            Easy.Text.show(message)
            return True
            
        except Exception as e:
            logging.error(f"Failed to send to sign: {e}")
            return False
    
    def handle_status_request(self):
        """Handle status requests"""
        try:
            status = {
                'service': 'Alpha Sign HTTP Service',
                'version': '1.0.0',
                'sign_connected': self.sign_connection is not None,
                'available_connections': Sign.get_available_connections(),
                'serial_available': Sign.is_serial_available()
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(status, indent=2).encode())
            
        except Exception as e:
            logging.error(f"Error handling status request: {e}")
            self.send_error(500, f"Error: {str(e)}")
    
    def handle_help_request(self):
        """Handle help requests"""
        help_text = """
Alpha Sign HTTP Service Help

Endpoints:
- GET /AlphaSign?msg=<message> - Send message to sign
- GET /status - Get service status
- GET /help - Show this help

AlphaSign Parameters:
- msg (required): The message to display
- color: red, green, amber, yellow, orange, auto, rain1, rain2, mix
- effect: scroll, hold, flash, roll_up, roll_down, roll_left, roll_right, wipe_up, wipe_down, wipe_left, wipe_right, twinkle, sparkle, snow, auto
- speed: 1-5 (1=slowest, 5=fastest)
- font: sans5, sans7, serif7, serif16, sans16
- line: top, middle, bottom, fill
- beep: 0-9 (number of beeps)
- label: A-Z (file label)

Examples:
- /AlphaSign?msg=Hello World
- /AlphaSign?msg=Hello&color=red&effect=flash&speed=5
- /AlphaSign?msg=Welcome&color=green&effect=twinkle&beep=3
- /AlphaSign?msg=Alert&color=amber&effect=hold&line=top

Special formatting in messages:
- <C:RED>text</C:RED> - Red text
- <SPEED:1>text</SPEED:1> - Slow speed
- <FLASH>text</FLASH> - Flash effect
- <TIME> - Current time
- <DATE> - Current date
- <ANIM:WELCOME> - Welcome animation
- <ANIM:FIREWORKS> - Fireworks animation
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(help_text.encode())

class AlphaSignHTTPService:
    """Main HTTP service class"""
    
    def __init__(self, host='0.0.0.0', port=8888, sign_ip='192.168.133.54', sign_port=10001):
        self.host = host
        self.port = port
        self.sign_ip = sign_ip
        self.sign_port = sign_port
        self.server = None
        self.running = False
        
        # Setup logging
        import platform
        
        # Determine log file path based on OS
        if platform.system() == 'Windows':
            log_file = os.path.join(os.getcwd(), 'alphasign-http.log')
        else:
            log_file = '/var/log/alphasign-http.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('AlphaSignHTTP')
    
    def start(self):
        """Start the HTTP service"""
        try:
            self.server = HTTPServer((self.host, self.port), AlphaSignHTTPHandler)
            self.running = True
            
            self.logger.info(f"Starting Alpha Sign HTTP Service on {self.host}:{self.port}")
            self.logger.info(f"Sign connection: {self.sign_ip}:{self.sign_port}")
            
            # Test sign connection
            try:
                test_sign = AlphaSign(port=f'{self.sign_ip}:{self.sign_port}')
                self.logger.info("Sign connection test successful")
            except Exception as e:
                self.logger.warning(f"Sign connection test failed: {e}")
            
            self.server.serve_forever()
            
        except KeyboardInterrupt:
            self.logger.info("Received interrupt signal")
            self.stop()
        except Exception as e:
            self.logger.error(f"Service error: {e}")
            raise
    
    def stop(self):
        """Stop the HTTP service"""
        if self.server:
            self.logger.info("Stopping Alpha Sign HTTP Service")
            self.server.shutdown()
            self.server.server_close()
            self.running = False
    
    def run(self):
        """Run the service (for systemd)"""
        self.start()

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Alpha Sign HTTP Service')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8888, help='Port to bind to (default: 8888)')
    parser.add_argument('--sign-ip', default='192.168.133.54', help='Alpha sign IP address')
    parser.add_argument('--sign-port', type=int, default=10001, help='Alpha sign port')
    parser.add_argument('--daemon', action='store_true', help='Run as daemon')
    
    args = parser.parse_args()
    
    service = AlphaSignHTTPService(
        host=args.host,
        port=args.port,
        sign_ip=args.sign_ip,
        sign_port=args.sign_port
    )
    
    if args.daemon:
        import daemon
        with daemon.DaemonContext():
            service.run()
    else:
        service.run()

if __name__ == '__main__':
    main()
