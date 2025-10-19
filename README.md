# python-alphasign

## What is it

This is a python 3 library that implements the "Alpha® Sign Communications Protocol" as defined [On alphasign website](https://alpha-american.com/p-alpha-communications-protocol.html).

This was tested on an Alpha 210C sign, and should works with other signs (like the BetaBrite) as well.

Documentation is available in the `docs/` dir

## Quickstart/Easy guide

python-alphasign implements so-called Easy classes, which enables easy functions to send text, show images and other functions easily.

Examples are available in examples/ (easy demos starts with `easy_`)

## Connection Types

The library now supports both traditional serial connections and IP connections for serial-over-IP converters:

### IP Connection (Default - No Additional Dependencies)
```python
from alphasign import AlphaSign, Easy

# IP connection with explicit port
sign = AlphaSign(port='192.168.133.54:10001')
Easy.Text.show('Hello World over IP!')

# IP connection with default port (10001)
sign = AlphaSign(port='192.168.133.54')
Easy.Text.show('Hello World over IP!')
```

### Serial Connection (Requires pyserial)
```python
from alphasign import AlphaSign, Easy

# Traditional serial connection (requires: pip install pyserial)
sign = AlphaSign(port='/dev/ttyUSB0')  # Linux
# sign = AlphaSign(port='COM1')        # Windows
Easy.Text.show('Hello World!')
```

## Dependencies

### Core Dependencies (Always Required)
- `Pillow` - Image processing
- `numpy` - Numerical operations

### Optional Dependencies
- `pyserial` - Only needed for serial connections
  ```bash
  pip install pyserial  # For serial connections
  ```

### Installation Options
```bash
# IP-only installation (no serial support)
pip install -r requirements.txt

# Full installation (with serial support)
pip install -r requirements.txt
pip install -r requirements-serial.txt
```

The library automatically detects the connection type based on the port parameter:
- IP addresses or hostnames with `:` → IP connection
- Device paths like `/dev/ttyUSB0`, `COM1` → Serial connection (requires pyserial)

## TODO

* Implement proper text parsing for special chars
* Implement features checks (for alpha 2.0 and 3.0 protocols, and sign-specific features)
* Implement LARGE DOTS, RGB DOTS and ALPHAVISION BULLETIN commands
* Implement image compression
* Implement read functions
* Implement counters and date
* Finish implementing the special functions
* Create abstraction classes for special functions (time/date, counters, memory config, buzzer, sequence and timetables, hardware functions...)
* Find out bugs with nested commands (doesn't work at all?) and pictures in slot other than A (doesn't config and/or display)

## Notes

* The "ASCII PRINTABLE" formats (2 and 3 bytes) aren't used because we can raw bytes
* * This mode was designed for POCSAG pagers, which can't send bytes < 0x20
