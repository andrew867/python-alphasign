import time
import socket
import re

# Try to import pyserial, but don't fail if it's not available
try:
    import serial
    PYSERIAL_AVAILABLE = True
except ImportError:
    PYSERIAL_AVAILABLE = False
    serial = None

from .singleton import Singleton
from .type import SignType
from .packet import Packet
from .ip_connection import IPConnection

class Sign(metaclass=Singleton):

    def __init__(self, type=SignType.All, address="00"):
        # Update self with properties from type class
        self.update_type(type)

        # Add address
        self.address = address
        
        # Connection objects
        self._ser = None
        self._ip_conn = None
        self._connection_type = None

    @classmethod
    def get_available_connections(cls):
        """Get list of available connection types"""
        connections = ['ip']  # IP is always available
        if PYSERIAL_AVAILABLE:
            connections.append('serial')
        return connections

    @classmethod
    def is_serial_available(cls):
        """Check if serial connections are available"""
        return PYSERIAL_AVAILABLE

    def _detect_connection_type(self, port):
        """
        Detect if port parameter is for serial or IP connection
        Returns: 'serial' or 'ip'
        """
        if not port:
            return 'serial'  # Default to serial if no port specified
            
        # Check if it's an IP address with port (format: ip:port or hostname:port)
        if ':' in port and not port.startswith('/'):
            return 'ip'
            
        # Check if it's a valid IP address
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(ip_pattern, port):
            return 'ip'
            
        # Check if it's a hostname (contains letters)
        if re.search(r'[a-zA-Z]', port) and '.' in port:
            return 'ip'
            
        # Default to serial for device paths like /dev/ttyUSB0, COM1, etc.
        return 'serial'

    def _parse_ip_connection(self, port):
        """
        Parse IP connection string to extract host and port
        Supports formats: 'host:port', 'ip:port', or just 'ip' (uses default port 10001)
        """
        if ':' in port:
            host, port_num = port.split(':', 1)
            return host, int(port_num)
        else:
            # Just IP address, use default port
            return port, 10001

    # Open serial or IP connection
    def open(self, port=None, **kwargs):
        self._connection_type = self._detect_connection_type(port)
        
        if self._connection_type == 'serial':
            if not PYSERIAL_AVAILABLE:
                raise ImportError(
                    "pyserial is not installed. Serial connections require pyserial. "
                    "Install with: pip install pyserial\n"
                    "Or use IP connection instead: port='192.168.133.54:10001'"
                )
            if self.connection == 'serial':
                self._ser = serial.Serial(port, self.default_baudrate, timeout=1)
            else:
                print("ERROR: no connection type?!?")
        elif self._connection_type == 'ip':
            host, port_num = self._parse_ip_connection(port)
            self._ip_conn = IPConnection(host, port_num, timeout=1)
            self._ip_conn.open()
        else:
            print("ERROR: unknown connection type?!?")

    def update_type(self, type):
        # Copy type's attributes as own
        props = [x for x in dir(type) if not x.startswith("__")]
        for prop in props:
            setattr(self, prop, getattr(type, prop))

    # Actually sends data
    def write(self, data):
        if self._connection_type == 'serial' and self._ser:
            self._ser.write(data)
        elif self._connection_type == 'ip' and self._ip_conn:
            self._ip_conn.write(data)
        else:
            print(f"ERROR sending data to {self._connection_type} link")

    # Send either raw data or packet, with pauses
    def send(self, data):
        # Packet or raw
        bytes = data.to_bytes() if isinstance(data, Packet) else data

        parts = bytes.split(b"\xFF")
        for part in parts:
            self.write(part)
            time.sleep(0.1)


    # TODO: be able to parse and send Packet back
    def read(self, raw=True):
        if self._connection_type == 'serial' and self._ser:
            if raw:
                return self._ser.read()
        elif self._connection_type == 'ip' and self._ip_conn:
            if raw:
                return self._ip_conn.read()

    def close(self):
        if self._connection_type == 'serial' and self._ser:
            self._ser.close()
        elif self._connection_type == 'ip' and self._ip_conn:
            self._ip_conn.close()
