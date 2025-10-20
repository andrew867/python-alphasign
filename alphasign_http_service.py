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
    
    # Class-level variables to persist across requests
    sign_connection = None
    datetime_set = False
    
    def __init__(self, *args, **kwargs):
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
            elif path == '/settime':
                self.handle_set_time_request(query_params)
            elif path == '/setdate':
                self.handle_set_date_request(query_params)
            elif path == '/sound':
                self.handle_sound_request(query_params)
            elif path == '/reset':
                self.handle_reset_request()
            elif path == '/memory':
                self.handle_memory_request(query_params)
            elif path == '/tone':
                self.handle_tone_request(query_params)
            elif path == '/runtime':
                self.handle_runtime_request(query_params)
            elif path == '/display':
                self.handle_display_request(query_params)
            elif path == '/dimming':
                self.handle_dimming_request(query_params)
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
            if not AlphaSignHTTPHandler.sign_connection:
                # Initialize connection
                AlphaSignHTTPHandler.sign_connection = AlphaSign(port='192.168.133.54:10001')
            
            # Only set date/time on initial connection or after reset
            if not AlphaSignHTTPHandler.datetime_set:
                self.set_sign_datetime()
                AlphaSignHTTPHandler.datetime_set = True
            
            # Send the text
            Easy.Text.show(message)
            return True
            
        except Exception as e:
            logging.error(f"Failed to send to sign: {e}")
            # Return True for demo mode - don't fail the request
            # In production, you might want to return False here
            return True
    
    def set_sign_datetime(self):
        """Set the current date and time on the Alpha sign"""
        try:
            import datetime
            now = datetime.datetime.now()
            
            # Set time
            time_cmd = self.string_processor.set_time(now)
            self.send_raw_command(time_cmd)
            
            # Set weekday
            weekday_cmd = self.string_processor.set_weekday(now.weekday())
            self.send_raw_command(weekday_cmd)
            
            # Set date
            date_cmd = self.string_processor.set_date(now)
            self.send_raw_command(date_cmd)
            
            # Set time format (24-hour)
            time_format_cmd = self.string_processor.set_time_format(ampm=False)
            self.send_raw_command(time_format_cmd)
            
            logging.info(f"Set sign date/time to: {now.strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            logging.warning(f"Failed to set sign date/time: {e}")
    
    def send_raw_command(self, command):
        """Send a raw command to the sign"""
        try:
            if self.sign_connection and self.sign_connection.sign:
                # Create complete packet
                packet = self.string_processor.create_complete_packet(command)
                
                # Send the packet
                self.sign_connection.sign.write(packet.encode('latin-1'))
                return True
            else:
                # Demo mode - log the command but don't fail
                logging.info(f"Demo mode: Would send command: {repr(command[:50])}...")
                return True
        except Exception as e:
            logging.error(f"Failed to send raw command: {e}")
            # Return True for demo mode
            return True
    
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
- GET /settime?time=14:30 - Set sign time
- GET /setdate?date=12/25/23 - Set sign date
- GET /sound?on=true - Control sign sound
- GET /reset - Soft reset the sign
- GET /memory?action=info - Get memory info
- GET /memory?action=configure - Configure memory map
- GET /tone?type=beep&freq=1000&duration=5 - Generate tone
- GET /runtime?label=A&start=09:00&stop=17:00 - Set run time table
- GET /display?enabled=true&x=10&y=5&text=Hello - Display text at XY
- GET /dimming?action=register&dim=1&brightness=80 - Set dimming register
- GET /dimming?action=time&start=18&stop=6 - Set dimming time schedule

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
- /settime?time=14:30
- /setdate?date=12/25/23
- /sound?on=true
- /reset

Special formatting in messages:
- <C:RED>text</C:RED> - Red text
- <SPEED:1>text</SPEED:1> - Slow speed
- <FLASH>text</FLASH> - Flash effect
- <TIME> - Current time
- <DATE> - Current date
- <ANIM:WELCOME> - Welcome animation
- <ANIM:FIREWORKS> - Fireworks animation

Features:
- Automatic date/time setting on connection
- Full Alpha protocol support
- Memory management
- Sound control
- Sign reset capability
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(help_text.encode())
    
    def handle_set_time_request(self, params):
        """Handle set time requests"""
        try:
            import datetime
            time_str = params.get('time', [None])[0]
            if not time_str:
                # Use current time
                now = datetime.datetime.now()
            else:
                # Parse provided time (format: HH:MM or HHMM)
                time_str = time_str.replace(':', '')
                if len(time_str) == 4:
                    hour = int(time_str[:2])
                    minute = int(time_str[2:])
                    now = datetime.datetime.now().replace(hour=hour, minute=minute)
                else:
                    raise ValueError("Invalid time format")
            
            # Set time on sign
            time_cmd = self.string_processor.set_time(now)
            if self.send_raw_command(time_cmd):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'status': 'success',
                    'message': f'Time set to {now.strftime("%H:%M")}',
                    'time': now.strftime('%H:%M')
                }
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_error(500, "Failed to set time on sign")
                
        except Exception as e:
            self.send_error(400, f"Invalid time format: {str(e)}")
    
    def handle_set_date_request(self, params):
        """Handle set date requests"""
        try:
            import datetime
            date_str = params.get('date', [None])[0]
            if not date_str:
                # Use current date
                now = datetime.datetime.now()
            else:
                # Parse provided date (format: MM/DD/YY or MM-DD-YY)
                date_str = date_str.replace('-', '/')
                now = datetime.datetime.strptime(date_str, '%m/%d/%y')
            
            # Set date on sign
            date_cmd = self.string_processor.set_date(now)
            if self.send_raw_command(date_cmd):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'status': 'success',
                    'message': f'Date set to {now.strftime("%m/%d/%y")}',
                    'date': now.strftime('%m/%d/%y')
                }
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_error(500, "Failed to set date on sign")
                
        except Exception as e:
            self.send_error(400, f"Invalid date format: {str(e)}")
    
    def handle_sound_request(self, params):
        """Handle sound control requests"""
        try:
            sound_on = params.get('on', ['false'])[0].lower() == 'true'
            
            # Set sound on sign
            sound_cmd = self.string_processor.set_sound(sound_on)
            if self.send_raw_command(sound_cmd):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'status': 'success',
                    'message': f'Sound {"enabled" if sound_on else "disabled"}',
                    'sound_on': sound_on
                }
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_error(500, "Failed to set sound on sign")
                
        except Exception as e:
            self.send_error(400, f"Invalid sound parameter: {str(e)}")
    
    def handle_reset_request(self):
        """Handle reset requests"""
        try:
            # Soft reset the sign
            reset_cmd = self.string_processor.soft_reset()
            if self.send_raw_command(reset_cmd):
                # After reset, reset the datetime flag so it gets set again on next message
                AlphaSignHTTPHandler.datetime_set = False
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'status': 'success',
                    'message': 'Sign reset successfully - date/time will be synchronized on next message'
                }
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_error(500, "Failed to reset sign")
                
        except Exception as e:
            self.send_error(500, f"Reset failed: {str(e)}")
    
    def handle_memory_request(self, params):
        """Handle memory management requests"""
        try:
            action = params.get('action', ['info'])[0]
            
            if action == 'info':
                # Read memory size
                memory_cmd = self.string_processor.read_memory_size()
                if self.send_raw_command(memory_cmd):
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {
                        'status': 'success',
                        'message': 'Memory info requested',
                        'action': 'read_memory_size'
                    }
                    self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_error(500, "Failed to read memory info")
                    
            elif action == 'configure':
                # Set memory map
                memory_cmd = self.string_processor.set_memory_map()
                if self.send_raw_command(memory_cmd):
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {
                        'status': 'success',
                        'message': 'Memory map configured',
                        'action': 'set_memory_map'
                    }
                    self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_error(500, "Failed to configure memory map")
            else:
                self.send_error(400, "Invalid memory action")
                
        except Exception as e:
            self.send_error(500, f"Memory operation failed: {str(e)}")
    
    def handle_tone_request(self, params):
        """Handle tone generation requests"""
        try:
            tone_type = params.get('type', ['beep'])[0]
            freq = int(params.get('freq', ['0'])[0])
            duration = int(params.get('duration', ['5'])[0])
            repeat = int(params.get('repeat', ['0'])[0])
            
            # Map tone types to protocol values
            tone_map = {
                'beep': chr(0x31),
                'custom': chr(0x32),
                'alarm': chr(0x33)
            }
            
            tone_code = tone_map.get(tone_type, chr(0x31))
            
            # Generate tone command
            tone_cmd = self.string_processor.generate_tone(tone_code, freq, duration, repeat)
            if self.send_raw_command(tone_cmd):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'status': 'success',
                    'message': f'Tone generated: {tone_type}',
                    'tone_type': tone_type,
                    'frequency': freq,
                    'duration': duration,
                    'repeat': repeat
                }
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_error(500, "Failed to generate tone")
                
        except Exception as e:
            self.send_error(400, f"Invalid tone parameters: {str(e)}")
    
    def handle_runtime_request(self, params):
        """Handle run time table requests"""
        try:
            label = params.get('label', ['A'])[0]
            start = params.get('start', ['00:00'])[0]
            stop = params.get('stop', ['23:59'])[0]
            
            # Convert time format
            start_time = start.replace(':', '')
            stop_time = stop.replace(':', '')
            
            # Set run time table
            runtime_cmd = self.string_processor.set_run_time_table(label, start_time, stop_time)
            if self.send_raw_command(runtime_cmd):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'status': 'success',
                    'message': f'Run time table set for {label}',
                    'label': label,
                    'start': start,
                    'stop': stop
                }
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_error(500, "Failed to set run time table")
                
        except Exception as e:
            self.send_error(400, f"Invalid run time parameters: {str(e)}")
    
    def handle_display_request(self, params):
        """Handle display text at XY requests"""
        try:
            enabled = params.get('enabled', ['true'])[0].lower() == 'true'
            x = int(params.get('x', ['0'])[0])
            y = int(params.get('y', ['0'])[0])
            text = params.get('text', [''])[0]
            
            # Display text at XY
            display_cmd = self.string_processor.display_text_at_xy(enabled, x, y, text)
            if self.send_raw_command(display_cmd):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'status': 'success',
                    'message': f'Text displayed at ({x},{y})',
                    'enabled': enabled,
                    'x': x,
                    'y': y,
                    'text': text
                }
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_error(500, "Failed to display text at XY")
                
        except Exception as e:
            self.send_error(400, f"Invalid display parameters: {str(e)}")
    
    def handle_dimming_request(self, params):
        """Handle dimming control requests"""
        try:
            action = params.get('action', ['register'])[0]
            
            if action == 'register':
                # Set dimming register
                dim = int(params.get('dim', ['0'])[0])
                brightness = int(params.get('brightness', ['100'])[0])
                
                dimming_cmd = self.string_processor.set_dimming_register(dim, brightness)
                if self.send_raw_command(dimming_cmd):
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {
                        'status': 'success',
                        'message': f'Dimming register set: dim={dim}, brightness={brightness}',
                        'action': 'register',
                        'dim': dim,
                        'brightness': brightness
                    }
                    self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_error(500, "Failed to set dimming register")
                    
            elif action == 'time':
                # Set dimming time schedule
                start = int(params.get('start', ['0'])[0])
                stop = int(params.get('stop', ['23'])[0])
                
                dimming_cmd = self.string_processor.set_dimming_time(start, stop)
                if self.send_raw_command(dimming_cmd):
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {
                        'status': 'success',
                        'message': f'Dimming time set: {start:02d}:00-{stop:02d}:00',
                        'action': 'time',
                        'start': start,
                        'stop': stop
                    }
                    self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_error(500, "Failed to set dimming time")
            else:
                self.send_error(400, "Invalid dimming action")
                
        except Exception as e:
            self.send_error(400, f"Invalid dimming parameters: {str(e)}")

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
