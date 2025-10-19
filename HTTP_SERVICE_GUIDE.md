# Alpha Sign HTTP Service Guide

A complete HTTP API for controlling Alpha LED signs via web requests. This service provides a RESTful interface to send messages, control colors, effects, and animations to Alpha signs over IP connections.

## Features

- **HTTP API**: Simple RESTful interface for controlling Alpha signs
- **String Processing**: Advanced text formatting with Alpha sign commands
- **Systemd Integration**: Runs as a system service with automatic startup
- **IP Connectivity**: Works with serial-over-IP converters
- **Comprehensive Parameters**: Support for all Alpha sign features
- **Error Handling**: Robust error handling and logging
- **Status Monitoring**: Built-in status and health endpoints

## Installation

### Quick Install
```bash
# Clone the repository
git clone <repository-url>
cd python-alphasign-1

# Run the installation script
sudo ./install_http_service.sh
```

### Manual Installation

**Linux/Unix:**
```bash
# Create service user
sudo useradd --system --no-create-home --shell /bin/false alphasign

# Create directories
sudo mkdir -p /opt/alphasign
sudo mkdir -p /var/log

# Copy files
sudo cp alphasign_http_service.py /opt/alphasign/
sudo cp -r alphasign /opt/alphasign/
sudo cp alphasign-http.service /etc/systemd/system/

# Install dependencies
sudo pip3 install -r requirements.txt

# Set permissions
sudo chown -R alphasign:alphasign /opt/alphasign
sudo chown alphasign:alphasign /var/log/alphasign-http.log

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable alphasign-http
sudo systemctl start alphasign-http
```

**Windows:**
```cmd
REM Run as Administrator
install_http_service_windows.bat

REM Or manually:
REM 1. Create directory: C:\alphasign
REM 2. Copy files to C:\alphasign\
REM 3. Install dependencies: pip install -r requirements.txt
REM 4. Run service: python alphasign_http_service.py
```

## Configuration

### Service Configuration

**Linux/Unix:**
Edit `/etc/systemd/system/alphasign-http.service` to modify:
- Host and port binding
- Alpha sign IP address and port
- Logging configuration
- Resource limits

**Windows:**
- Logs are automatically written to the current directory (`alphasign-http.log`)
- Use `install_http_service_windows.bat` for Windows installation
- Service can be run manually or installed as Windows service using NSSM

### Alpha Sign Connection
The service connects to your Alpha sign via IP. Default configuration:
- **Sign IP**: 192.168.133.54
- **Sign Port**: 10001
- **Service Port**: 8888

## API Endpoints

### Main Endpoint: `/AlphaSign`
Send messages to the Alpha sign with various formatting options.

**Method**: GET  
**Parameters**:
- `msg` (required): The message to display
- `color`: Text color (red, green, amber, yellow, orange, auto, rain1, rain2, mix)
- `effect`: Display effect (scroll, hold, flash, roll_up, roll_down, etc.)
- `speed`: Animation speed (1-5, where 1=slowest, 5=fastest)
- `font`: Text font (sans5, sans7, serif7, serif16, sans16)
- `line`: Line position (top, middle, bottom, fill)
- `beep`: Number of beeps (0-9)
- `label`: File label (A-Z)

### Status Endpoint: `/status`
Get service status and connection information.

**Method**: GET  
**Response**: JSON with service status, version, and connection info

### Help Endpoint: `/help`
Get detailed API documentation and examples.

**Method**: GET  
**Response**: Plain text help documentation

## Usage Examples

### Basic Message
```bash
curl "http://localhost:8888/AlphaSign?msg=Hello World"
```

### Colored Message with Effect
```bash
curl "http://localhost:8888/AlphaSign?msg=Welcome&color=red&effect=flash&speed=5"
```

### Multi-line Message
```bash
curl "http://localhost:8888/AlphaSign?msg=Line 1\\nLine 2&line=top"
```

### Message with Beep
```bash
curl "http://localhost:8888/AlphaSign?msg=Alert&color=amber&beep=3"
```

### Advanced Formatting
```bash
curl "http://localhost:8888/AlphaSign?msg=Welcome&color=green&effect=twinkle&font=sans16&speed=3&line=fill"
```

## Advanced String Formatting

The service supports advanced Alpha sign formatting codes:

### Colors
- `<C:RED>text</C:RED>` - Red text
- `<C:GREEN>text</C:GREEN>` - Green text
- `<C:AMBER>text</C:AMBER>` - Amber text
- `<C:YELLOW>text</C:YELLOW>` - Yellow text
- `<C:AUTO>text</C:AUTO>` - Auto color

### Effects
- `<SCROLL>` - Scroll effect
- `<HOLD>` - Hold effect
- `<FLASH>` - Flash effect
- `<TWINKLE>` - Twinkle effect
- `<SPARKLE>` - Sparkle effect
- `<SNOW>` - Snow effect

### Speed Control
- `<SPEED:1>` - Slowest speed
- `<SPEED:2>` - Slow speed
- `<SPEED:3>` - Medium speed
- `<SPEED:4>` - Fast speed
- `<SPEED:5>` - Fastest speed

### Fonts
- `<F:SANS5>` - 5x7 Sans font
- `<F:SANS7>` - 7x7 Sans font
- `<F:SERIF7>` - 7x7 Serif font
- `<F:SERIF16>` - 16x16 Serif font
- `<F:SANS16>` - 16x16 Sans font

### Special Characters
- `<TIME>` - Current time
- `<DATE>` - Current date
- `<BEEP:3>` - 3 beeps
- `\\n` - New line
- `\\p` - Page break

### Animations
- `<ANIM:WELCOME>` - Welcome animation
- `<ANIM:THANKYOU>` - Thank you animation
- `<ANIM:FIREWORKS>` - Fireworks animation
- `<ANIM:SLOTS>` - Slot machine animation

## Service Management

### Start Service
```bash
sudo systemctl start alphasign-http
```

### Stop Service
```bash
sudo systemctl stop alphasign-http
```

### Restart Service
```bash
sudo systemctl restart alphasign-http
```

### Check Status
```bash
sudo systemctl status alphasign-http
```

### View Logs

**Linux/Unix:**
```bash
# View recent logs
sudo journalctl -u alphasign-http -f

# View all logs
sudo journalctl -u alphasign-http

# View service log file
sudo tail -f /var/log/alphasign-http.log
```

**Windows:**
```cmd
REM View log file
type alphasign-http.log

REM View log in real-time (if available)
powershell Get-Content alphasign-http.log -Wait

REM View log with more
more alphasign-http.log
```

### Enable Auto-start
```bash
sudo systemctl enable alphasign-http
```

## Testing

### Run Test Suite
```bash
# Run all tests
python3 test_http_service.py

# Run quick tests
python3 test_http_service.py --quick

# Test remote service
python3 test_http_service.py --url http://remote-server:8888
```

### Manual Testing
```bash
# Test basic functionality
curl "http://localhost:8888/AlphaSign?msg=Test Message"

# Check service status
curl "http://localhost:8888/status"

# Get help
curl "http://localhost:8888/help"
```

## Troubleshooting

### Service Won't Start
1. Check if port 8888 is available:
   ```bash
   sudo netstat -tlnp | grep 8888
   ```

2. Check service logs:
   ```bash
   sudo journalctl -u alphasign-http -n 50
   ```

3. Verify Alpha sign connectivity:
   ```bash
   ping 192.168.133.54
   telnet 192.168.133.54 10001
   ```

### Connection Issues
1. Verify Alpha sign IP and port configuration
2. Check firewall settings
3. Ensure serial-over-IP converter is running
4. Test network connectivity

### Permission Issues
1. Check file permissions:
   ```bash
   sudo chown -R alphasign:alphasign /opt/alphasign
   ```

2. Verify service user exists:
   ```bash
   id alphasign
   ```

### Performance Issues
1. Check system resources:
   ```bash
   sudo systemctl status alphasign-http
   ```

2. Monitor log file size:
   ```bash
   ls -lh /var/log/alphasign-http.log
   ```

## Security Considerations

- The service runs as a non-privileged user (`alphasign`)
- Limited file system access with `ProtectSystem=strict`
- No network access to external services
- Log files are properly secured
- Resource limits prevent abuse

## Integration Examples

### Home Assistant
```yaml
# configuration.yaml
rest_command:
  alpha_sign:
    url: "http://localhost:8888/AlphaSign"
    method: GET
    params:
      msg: "{{ message }}"
      color: "{{ color }}"
      effect: "{{ effect }}"

# Usage in automations
automation:
  - alias: "Alpha Sign Alert"
    trigger:
      - platform: state
        entity_id: binary_sensor.door
        to: 'on'
    action:
      - service: rest_command.alpha_sign
        data:
          message: "Door Open!"
          color: "red"
          effect: "flash"
```

### Node-RED
```javascript
// HTTP Request node configuration
// URL: http://localhost:8888/AlphaSign
// Method: GET
// Parameters:
//   msg: {{payload.message}}
//   color: {{payload.color}}
//   effect: {{payload.effect}}
```

### Python Script
```python
import requests

def send_to_alpha_sign(message, color='auto', effect='scroll'):
    url = "http://localhost:8888/AlphaSign"
    params = {
        'msg': message,
        'color': color,
        'effect': effect
    }
    response = requests.get(url, params=params)
    return response.json()

# Usage
result = send_to_alpha_sign("Hello World", "red", "flash")
print(result)
```

## API Reference

### Response Format
All successful requests return JSON:
```json
{
  "status": "success",
  "message": "Text sent to Alpha sign",
  "original": "Hello World",
  "processed": "Processed message with formatting"
}
```

### Error Responses
- **400 Bad Request**: Missing required parameters
- **404 Not Found**: Invalid endpoint
- **500 Internal Server Error**: Service or sign connection error

### Rate Limiting
The service includes built-in delays between requests to prevent overwhelming the Alpha sign. Typical response time is 1-2 seconds per request.

## Contributing

To contribute to the HTTP service:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the Apache License 2.0. See the LICENSE file for details.
