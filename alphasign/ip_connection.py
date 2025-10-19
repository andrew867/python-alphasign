import socket
import time

class IPConnection:
    """
    Serial over IP connection class that mimics pyserial interface
    for use with serial-to-IP converters.
    """
    
    def __init__(self, host, port, timeout=1):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket = None
        self._is_open = False
    
    def open(self):
        """Open socket connection to IP serial converter"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.host, self.port))
            self._is_open = True
        except Exception as e:
            raise ConnectionError(f"Failed to connect to {self.host}:{self.port} - {e}")
    
    def write(self, data):
        """Write data to the IP connection"""
        if not self._is_open or not self.socket:
            raise ConnectionError("Connection not open")
        
        try:
            self.socket.send(data)
        except Exception as e:
            raise ConnectionError(f"Failed to write data: {e}")
    
    def read(self, size=1):
        """Read data from the IP connection"""
        if not self._is_open or not self.socket:
            raise ConnectionError("Connection not open")
        
        try:
            return self.socket.recv(size)
        except socket.timeout:
            return b""
        except Exception as e:
            raise ConnectionError(f"Failed to read data: {e}")
    
    def close(self):
        """Close the IP connection"""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
        self._is_open = False
    
    @property
    def is_open(self):
        """Check if connection is open"""
        return self._is_open and self.socket is not None
