import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphasign import Sign, SignType, Text

# Open sign via IP connection
sign = Sign()
sign.open(port="192.168.133.54:10001")

# Send formatted text with colors
text = Text("{{red}}Hello{{green}}World over IP!")
sign.send(text.to_packet(label="0", mode=Text.Mode.rotate))
