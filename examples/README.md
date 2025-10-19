# Examples Directory

This directory contains example scripts demonstrating how to use the python-alphasign library.

## Running Examples

All examples are configured to automatically find the library in the parent directory, so you can run them directly:

```bash
# From the examples directory
cd examples
python easy_text.py
python easy_text_ip.py
python connection_comparison.py
```

Or from the project root:

```bash
# From the project root
python examples/easy_text.py
python examples/easy_text_ip.py
python examples/connection_comparison.py
```

## Example Files

### Serial Connection Examples
- **`easy_text.py`** - Simple text display via serial
- **`easy_image.py`** - Image display via serial  
- **`text_full.py`** - Advanced text formatting via serial

### IP Connection Examples
- **`easy_text_ip.py`** - Simple text display via IP
- **`easy_image_ip.py`** - Image display via IP
- **`text_full_ip.py`** - Advanced text formatting via IP

### Comparison Examples
- **`connection_comparison.py`** - Demonstrates both serial and IP connections

## Configuration

### Serial Examples
Update the port parameter to match your system:
- Linux: `'/dev/ttyUSB0'` or `'/dev/ttyACM0'`
- Windows: `'COM1'`, `'COM2'`, etc.
- macOS: `'/dev/tty.usbserial-*'`

### IP Examples
Update the IP address and port as needed:
- Default: `'192.168.133.54:10001'`
- Custom IP: `'your.ip.address:port'`
- Default port: `'192.168.133.54'` (uses port 10001)

## Testing

Run the test script to verify all examples work:

```bash
python test_examples.py
```

This will check:
- Python syntax validity
- Import path configuration
- Example file structure

## Troubleshooting

### Import Errors
If you get import errors, make sure you're running from the correct directory and that the alphasign library is in the parent directory.

### Connection Errors
- **Serial**: Check device permissions and port availability
- **IP**: Verify IP address, port, and network connectivity

### Permission Errors (Linux)
You may need to add your user to the dialout group:
```bash
sudo usermod -a -G dialout $USER
```
Then log out and back in.
