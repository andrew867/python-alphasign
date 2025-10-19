# IP Connection Guide

This guide explains how to use the new IP connection functionality in python-alphasign for communicating with Alpha signs via serial-over-IP converters.

## Overview

The library now supports both traditional serial connections and IP connections. The connection type is automatically detected based on the port parameter format.

## Connection Types

### Serial Connection (Traditional)
```python
from alphasign import AlphaSign, Easy

# Linux/Unix
sign = AlphaSign(port='/dev/ttyUSB0')
Easy.Text.show('Hello World!')

# Windows
sign = AlphaSign(port='COM1')
Easy.Text.show('Hello World!')
```

### IP Connection (New)
```python
from alphasign import AlphaSign, Easy

# IP connection with explicit port
sign = AlphaSign(port='192.168.133.54:10001')
Easy.Text.show('Hello World over IP!')

# IP connection with default port (10001)
sign = AlphaSign(port='192.168.133.54')
Easy.Text.show('Hello World over IP!')
```

## Automatic Detection

The library automatically detects the connection type:

| Port Format | Connection Type | Example |
|-------------|----------------|---------|
| `ip:port` | IP | `192.168.133.54:10001` |
| `ip` | IP (default port 10001) | `192.168.133.54` |
| `hostname:port` | IP | `sign.local:10001` |
| `/dev/tty*` | Serial | `/dev/ttyUSB0` |
| `COM*` | Serial | `COM1` |

## Default Configuration

- **Default IP Port**: 10001
- **Default IP Address**: 192.168.133.54 (as specified)
- **Timeout**: 1 second
- **Protocol**: TCP socket connection

## Examples

### Basic Text Display
```python
from alphasign import AlphaSign, Easy

# Connect via IP
sign = AlphaSign(port='192.168.133.54:10001')
Easy.Text.show('Hello from IP!')
```

### Image Display
```python
from alphasign import AlphaSign, Easy

# Connect via IP and show image
sign = AlphaSign(port='192.168.133.54')
Easy.Image.show('my_image.png')
```

### Advanced Usage
```python
from alphasign import Sign, SignType, Text

# Direct sign control
sign = Sign()
sign.open(port='192.168.133.54:10001')

# Send formatted text
text = Text("{{red}}Hello{{green}}World!")
sign.send(text.to_packet(label="0", mode=Text.Mode.rotate))
```

### Buzzer Control
```python
from alphasign import AlphaSign, Easy

sign = AlphaSign(port='192.168.133.54:10001')

# Enable buzzer
Easy.Buzzer.enable()

# Generate tone
Easy.Buzzer.beep(freq=1000, duration=2, repeat=1)
```

## Error Handling

The IP connection includes proper error handling:

```python
try:
    sign = AlphaSign(port='192.168.133.54:10001')
    Easy.Text.show('Test message')
except ConnectionError as e:
    print(f"Connection failed: {e}")
except Exception as e:
    print(f"Other error: {e}")
```

## Testing

Run the test script to verify IP connectivity:

```bash
python test_ip_connection.py
```

This will test:
- Connection type detection
- IP connection establishment
- Text display functionality
- Image functionality (if test image exists)
- Buzzer functionality

## Troubleshooting

### Connection Issues
- Verify the IP address and port are correct
- Check network connectivity: `ping 192.168.133.54`
- Verify the serial-over-IP converter is running
- Check firewall settings

### Port Issues
- Default port is 10001
- Ensure the port is not blocked by firewall
- Try different ports if the converter uses a different one

### Timeout Issues
- The default timeout is 1 second
- Increase timeout if needed by modifying the IPConnection class
- Check network latency

## Backward Compatibility

All existing serial-based code continues to work without modification. The IP functionality is purely additive and doesn't break existing functionality.
